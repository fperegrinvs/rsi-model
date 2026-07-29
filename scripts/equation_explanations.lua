-- Attach progressively enhanced, native-details explanations to numbered
-- equations. The explanation content is generated and validated from the
-- structured registries before Pandoc runs.

local explanation_files = {}
local equation_pages = {}
local seen = {}
local map_file = os.getenv("EQUATION_EXPLANATION_MAP_FILE")
local equation_map_file = os.getenv("EQUATION_MAP_FILE")

if map_file == nil or map_file == "" then
  error("EQUATION_EXPLANATION_MAP_FILE is required")
end

for line in io.lines(map_file) do
  local identifier, file = line:match("^([^\t]+)\t(.+)$")
  if identifier == nil or file == nil then
    error("malformed equation explanation map row")
  end
  if explanation_files[identifier] ~= nil then
    error("duplicate equation explanation map entry: " .. identifier)
  end
  explanation_files[identifier] = file
end

if equation_map_file ~= nil and equation_map_file ~= "" then
  for line in io.lines(equation_map_file) do
    local identifier, _, page = line:match("^([^\t]+)\t([^\t]+)\t?(.*)$")
    if identifier ~= nil and page ~= nil and page ~= "" then
      equation_pages[identifier] = page
    end
  end
end

local function normalized_input_file()
  local input = PANDOC_STATE.input_files[1] or ""
  if quarto ~= nil and quarto.doc ~= nil and quarto.doc.input_file ~= nil then
    input = quarto.doc.input_file
  end
  input = input:gsub("\\", "/")
  local project = os.getenv("SITE_PROJECT_DIR")
  if project ~= nil and project ~= "" then
    project = project:gsub("\\", "/"):gsub("/$", "")
    local prefix = project .. "/"
    if input:sub(1, #prefix) == prefix then
      input = input:sub(#prefix + 1)
    end
  end
  return input:gsub("%.qmd$", ".html"):gsub("%.md$", ".html")
end

local function directory_segments(file)
  local directory = file:match("^(.*)/[^/]+$") or ""
  local segments = {}
  for segment in directory:gmatch("[^/]+") do
    table.insert(segments, segment)
  end
  return segments
end

local function relative_page(from_page, to_page)
  if from_page == to_page then
    return ""
  end
  local from = directory_segments(from_page)
  local to = {}
  for segment in to_page:gmatch("[^/]+") do
    table.insert(to, segment)
  end
  local common = 0
  while common < #from and common < (#to - 1) and from[common + 1] == to[common + 1] do
    common = common + 1
  end
  local parts = {}
  for _ = common + 1, #from do
    table.insert(parts, "..")
  end
  for index = common + 1, #to do
    table.insert(parts, to[index])
  end
  return table.concat(parts, "/")
end

local function target_for_page(page, identifier)
  if os.getenv("QUARTO_SITE_MODE") ~= "1" then
    return "#" .. identifier
  end
  local relative = relative_page(normalized_input_file(), page)
  if relative == "" then
    return "#" .. identifier
  end
  return relative .. "#" .. identifier
end

local function has_class(element, class_name)
  for _, value in ipairs(element.classes) do
    if value == class_name then
      return true
    end
  end
  return false
end

local function read_file(file)
  local handle, message = io.open(file, "r")
  if handle == nil then
    error("cannot read equation explanation " .. file .. ": " .. message)
  end
  local content = handle:read("*a")
  handle:close()
  return content
end

local function explanation_fragment(identifier)
  local slug = identifier:gsub("^eq:", ""):gsub("[^A-Za-z0-9_-]", "-")
  return "explain-eq-" .. slug
end

function Pandoc(document)
  local rendered = document:walk({
    Div = function(div)
      if not has_class(div, "numbered-equation") then
        return div
      end
      local identifier = div.identifier
      local file = explanation_files[identifier]
      if file == nil then
        error("missing equation explanation for " .. identifier)
      end
      if seen[identifier] then
        error("duplicate rendered equation explanation for " .. identifier)
      end
      seen[identifier] = true
      local number = div.attributes["data-equation-number"]
      if number == nil or number == "" then
        error("equation explanation has no generated number: " .. identifier)
      end
      local fragment = explanation_fragment(identifier)
      local button = table.concat({
        '<div class="equation-explain-controls">',
        '<button type="button" class="equation-explain-button" ',
        'aria-expanded="false" aria-controls="' .. fragment .. '" ',
        'data-equation-explain="' .. fragment .. '">',
        'Explain equation (' .. number .. ")</button></div>",
      })
      local details_open = table.concat({
        '<details id="' .. fragment .. '" class="equation-explanation" ',
        'data-equation-explanation="' .. identifier .. '">',
        "<summary>Explain equation (" .. number .. ")</summary>",
      })
      div.content:insert(pandoc.RawBlock("html", button))
      div.content:insert(pandoc.RawBlock("html", details_open))
      local explanation = pandoc.read(read_file(file), "markdown"):walk({
        Link = function(link)
          local related = link.target:match("^equation:(eq:.+)$")
          if related ~= nil then
            link.target = target_for_page(
              equation_pages[related] or normalized_input_file(),
              related
            )
          elseif link.target == "notation:register" then
            link.target = target_for_page(
              "notation/index.html",
              "d.3-consolidated-notation"
            )
          end
          return link
        end,
      })
      for _, block in ipairs(explanation.blocks) do
        div.content:insert(block)
      end
      div.content:insert(pandoc.RawBlock("html", "</details>"))
      return div
    end,
  })

  for identifier, _ in pairs(explanation_files) do
    local required_on_page = (
      os.getenv("QUARTO_SITE_MODE") ~= "1" or
      equation_pages[identifier] == normalized_input_file()
    )
    if required_on_page and not seen[identifier] then
      error("stale equation explanation for " .. identifier)
    end
  end
  return rendered
end

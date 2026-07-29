-- Resolve semantic proposition pseudo-links in standalone and multi-page HTML.

local propositions = {}
local map_file = os.getenv("PROPOSITION_MAP_FILE")

if map_file == nil or map_file == "" then
  error("PROPOSITION_MAP_FILE is required")
end

for line in io.lines(map_file) do
  local identifier, title, anchor, status, page =
    line:match("^([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)$")
  if identifier == nil or title == nil or anchor == nil or status == nil or page == nil then
    error("malformed proposition map row")
  end
  if propositions[identifier] ~= nil then
    error("duplicate proposition map entry: " .. identifier)
  end
  propositions[identifier] = {
    title = title,
    anchor = anchor,
    status = status,
    page = page,
  }
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

local function target_for(proposition)
  if os.getenv("QUARTO_SITE_MODE") ~= "1" then
    return "#" .. proposition.anchor
  end
  local relative = relative_page(normalized_input_file(), proposition.page)
  if relative == "" then
    return "#" .. proposition.anchor
  end
  return relative .. "#" .. proposition.anchor
end

local function has_class(element, class_name)
  for _, value in ipairs(element.classes) do
    if value == class_name then
      return true
    end
  end
  return false
end

function Link(link)
  local identifier = link.target:match("^proposition:(P.+)$")
  if identifier == nil then
    return link
  end
  local proposition = propositions[identifier]
  if proposition == nil then
    error("undefined proposition reference: " .. identifier)
  end
  link.target = target_for(proposition)
  if not has_class(link, "proposition-ref") then
    link.classes:insert("proposition-ref")
  end
  link.attributes["aria-label"] = identifier .. " — " .. proposition.title
  link.attributes["title"] = proposition.status
  link.attributes["data-proposition"] = identifier
  return link
end

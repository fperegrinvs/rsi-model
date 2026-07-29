-- Deterministic global figure numbering and cross-page references for Pandoc 3.x.
--
-- Author figures as a captioned image with a semantic identifier:
--
--   ![Reader caption.](image.png){#fig-example .figure-standard fig-alt="Visual description."}
--
-- Cite them as `Figure [@fig-example]`. A FIGURE_MAP_FILE containing
-- identifier<TAB>number<TAB>output-page makes the multi-page Quarto build use
-- the same global order as the standalone manuscript.

local figure_numbers = {}
local figure_pages = {}
local seen_figures = {}
local figure_counter = 0

local figure_map_file = os.getenv("FIGURE_MAP_FILE")
if figure_map_file ~= nil and figure_map_file ~= "" then
  for line in io.lines(figure_map_file) do
    local identifier, number, page = line:match("^([^\t]+)\t([^\t]+)\t?(.*)$")
    if identifier ~= nil then
      figure_numbers[identifier] = number
      if page ~= nil and page ~= "" then
        figure_pages[identifier] = page
      end
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
  return input
end

local function current_output_page()
  return normalized_input_file():gsub("%.qmd$", ".html"):gsub("%.md$", ".html")
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
  local relative = relative_page(current_output_page(), page)
  if relative == "" then
    return "#" .. identifier
  end
  return relative .. "#" .. identifier
end

local function number_figure(figure)
  if figure.identifier == "" or not figure.identifier:match("^fig%-") then
    error("authored figure is missing a semantic fig- identifier")
  end
  if seen_figures[figure.identifier] then
    error("duplicate figure identifier: " .. figure.identifier)
  end
  seen_figures[figure.identifier] = true
  local presentation_class = nil
  figure.content = figure.content:walk({
    Image = function(image)
      local retained = {}
      for _, class_name in ipairs(image.classes) do
        if class_name:match("^figure%-") then
          if presentation_class ~= nil then
            error("figure has more than one presentation class: " .. figure.identifier)
          end
          presentation_class = class_name
        else
          table.insert(retained, class_name)
        end
      end
      image.classes = retained
      local visual_description = image.attributes["fig-alt"]
      if visual_description == nil or visual_description == "" then
        error("figure is missing fig-alt: " .. figure.identifier)
      end
      image.caption = {pandoc.Str(visual_description)}
      image.attributes["fig-alt"] = nil
      return image
    end,
  })
  if presentation_class == nil then
    error("figure is missing a presentation class: " .. figure.identifier)
  end
  figure.classes:insert(presentation_class)
  local number = figure_numbers[figure.identifier]
  if number == nil then
    figure_counter = figure_counter + 1
    number = tostring(figure_counter)
    figure_numbers[figure.identifier] = number
  end

  figure.classes:insert("numbered-figure")
  figure.attributes["data-figure-number"] = number
  if presentation_class == "figure-wide" then
    figure.content = figure.content:walk({
      Image = function(image)
        return pandoc.Link(
          {image},
          image.src,
          "Open full-resolution Figure " .. number,
          pandoc.Attr(
            "",
            {"figure-full-resolution-link"},
            {["aria-label"] = "Open Figure " .. number .. " at full resolution"}
          )
        )
      end,
    })
  end
  local label = pandoc.Link(
    {pandoc.Str("Figure " .. number)},
    "#" .. figure.identifier,
    "Figure " .. number,
    pandoc.Attr(
      "",
      {"figure-number"},
      {["aria-label"] = "Figure " .. number}
    )
  )
  local first = figure.caption.long[1]
  if first == nil or (first.t ~= "Plain" and first.t ~= "Para") then
    figure.caption.long:insert(1, pandoc.Plain({label, pandoc.Str(".")}))
  else
    first.content:insert(1, pandoc.Space())
    first.content:insert(1, pandoc.Str("."))
    first.content:insert(1, label)
  end
  return figure
end

local function replace_reference(citation)
  if #citation.citations ~= 1 then
    return citation
  end
  local identifier = citation.citations[1].id
  if not identifier:match("^fig%-") then
    return citation
  end
  local number = figure_numbers[identifier]
  if number == nil then
    error("unresolved figure reference: " .. identifier)
  end
  return pandoc.Link(
    {pandoc.Str(number)},
    target_for_page(figure_pages[identifier] or current_output_page(), identifier),
    "Figure " .. number,
    pandoc.Attr(
      "",
      {"figure-reference"},
      {["aria-label"] = "Go to figure " .. number}
    )
  )
end

local function number_document(document)
  local numbered = document:walk({Figure = number_figure})
  return numbered:walk({Cite = replace_reference})
end

return {{Pandoc = number_document}}

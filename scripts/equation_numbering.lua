-- Deterministic equation numbering and cross-references for Pandoc 3.x.
--
-- Numbered equations must be wrapped in a Div with class `equation` and an
-- identifier beginning `eq:`, for example:
--
--   ::: {#eq:capacity-growth .equation}
--   $$
--   ...
--   $$
--   :::
--
-- Cite them in prose as `Equation [@eq:capacity-growth]` or
-- `Eq. [@eq:capacity-growth]`. The filter replaces the citation with a
-- deep-linkable generated number.

local equation_numbers = {}
local equation_pages = {}
local seen_equations = {}
local main_counter = 0
local appendix_counters = {}
local current_appendix = nil

local equation_map_file = os.getenv("EQUATION_MAP_FILE")
if equation_map_file ~= nil and equation_map_file ~= "" then
  for line in io.lines(equation_map_file) do
    local identifier, number, page = line:match("^([^\t]+)\t([^\t]+)\t?(.*)$")
    if identifier ~= nil then
      equation_numbers[identifier] = number
      if page ~= nil and page ~= "" then
        equation_pages[identifier] = page
      end
    end
  end
end

local function normalized_input_file()
  local input = PANDOC_STATE.input_files[1] or ""
  if (
    quarto ~= nil and
    quarto.doc ~= nil and
    quarto.doc.input_file ~= nil
  ) then
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
  local input = normalized_input_file()
  input = input:gsub("%.qmd$", ".html")
  input = input:gsub("%.md$", ".html")
  return input
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
  while (
    common < #from and
    common < (#to - 1) and
    from[common + 1] == to[common + 1]
  ) do
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

local function has_class(element, class_name)
  for _, value in ipairs(element.classes) do
    if value == class_name then
      return true
    end
  end
  return false
end

local function equation_number()
  if current_appendix == nil then
    main_counter = main_counter + 1
    return tostring(main_counter)
  end
  local count = (appendix_counters[current_appendix] or 0) + 1
  appendix_counters[current_appendix] = count
  return current_appendix .. "." .. tostring(count)
end

local function source_marker_link(label, first_source)
  local inner = label:sub(2, -2)
  local link = pandoc.Link(
    {pandoc.Str(inner)},
    target_for_page("sources/index.html", "source-s" .. first_source),
    "Source " .. inner,
    pandoc.Attr(
      "",
      {"source-marker"},
      {["aria-label"] = "Go to source " .. inner}
    )
  )
  return {pandoc.Str("["), link, pandoc.Str("]")}
end

local function link_source_markers(value)
  local text = value.text
  local output = {}
  local cursor = 1
  local changed = false
  while cursor <= #text do
    local first, last, start_number, end_number = text:find(
      "%[S(%d+)[–%-]S?(%d+)%]",
      cursor
    )
    local single = false
    if first == nil then
      first, last, start_number = text:find("%[S(%d+)%]", cursor)
      single = true
    end
    if first == nil then
      if cursor <= #text then
        table.insert(output, pandoc.Str(text:sub(cursor)))
      end
      break
    end
    if first > cursor then
      table.insert(output, pandoc.Str(text:sub(cursor, first - 1)))
    end
    local label = text:sub(first, last)
    for _, inline in ipairs(source_marker_link(label, start_number)) do
      table.insert(output, inline)
    end
    changed = true
    cursor = last + 1
    if single then
      end_number = nil
    end
  end
  if changed then
    return output
  end
  return nil
end

local function number_document(document)
  local numbered = document:walk({
    Header = function(header)
      if header.level == 1 then
        local letter = pandoc.utils.stringify(header.content):match(
          "^Appendix%s+([A-Z])"
        )
        current_appendix = letter
      end
      return header
    end,
    Div = function(div)
      if not has_class(div, "equation") then
        return div
      end
      if div.identifier == "" or not div.identifier:match("^eq:") then
        error("numbered equation is missing a semantic eq: identifier")
      end
      if seen_equations[div.identifier] then
        error("duplicate equation identifier: " .. div.identifier)
      end
      seen_equations[div.identifier] = true
      local number = equation_numbers[div.identifier] or equation_number()
      equation_numbers[div.identifier] = number
      div.classes:insert("numbered-equation")
      div.attributes["data-equation-number"] = number
      local equation_body = div.content[1]
      if equation_body == nil then
        error("numbered equation has no mathematical content: " .. div.identifier)
      end
      div.content[1] = pandoc.Div(
        {equation_body},
        pandoc.Attr(
          "",
          {"equation-math-scroll"},
          {
            {"tabindex", "0"},
            {
              "aria-label",
              "Equation " .. number ..
                " mathematical expression; scroll horizontally if needed",
            },
          }
        )
      )
      div.content:insert(
        pandoc.Div(
          {pandoc.Plain({pandoc.Str("Scroll equation"), pandoc.Space(), pandoc.Str("→")})},
          pandoc.Attr("", {"equation-scroll-cue"}, {["aria-hidden"] = "true"})
        )
      )
      local label = pandoc.Link(
        {pandoc.Str("(" .. number .. ")")},
        "#" .. div.identifier,
        "Equation " .. number,
        pandoc.Attr(
          "",
          {"equation-label"},
          {["aria-label"] = "Equation " .. number}
        )
      )
      div.content:insert(
        pandoc.Div(
          {pandoc.Para({label})},
          pandoc.Attr("", {"equation-label-container"})
        )
      )
      return div
    end,
  })

  local referenced = numbered:walk({
    Cite = function(citation)
      if #citation.citations ~= 1 then
        return citation
      end
      local identifier = citation.citations[1].id
      if not identifier:match("^eq:") then
        return citation
      end
      local number = equation_numbers[identifier]
      if number == nil then
        error("unresolved equation reference: " .. identifier)
      end
      return pandoc.Link(
        {pandoc.Str("(" .. number .. ")")},
        target_for_page(
          equation_pages[identifier] or current_output_page(),
          identifier
        ),
        "Equation " .. number,
        pandoc.Attr(
          "",
          {"equation-reference"},
          {["aria-label"] = "Go to equation " .. number}
        )
      )
    end,
  })

  local notation_linked = referenced:walk({
    Div = function(div)
      if not has_class(div, "notation-register") then
        return div
      end
      return div:walk({
        Link = function(link)
          if not has_class(link, "equation-reference") then
            return link
          end
          local identifier = link.target:match("#(eq:[A-Za-z0-9_.:-]+)$")
          if identifier == nil then
            error("notation-register equation reference has no semantic target")
          end
          local number = equation_numbers[identifier]
          if number == nil then
            error("notation-register explanation has no equation number: " .. identifier)
          end
          local page = equation_pages[identifier] or current_output_page()
          local explanation = pandoc.Link(
            {pandoc.Str("explanation")},
            target_for_page(page, "explain-eq-" .. identifier:gsub("^eq:", "")),
            "Explain equation " .. number,
            pandoc.Attr(
              "",
              {"equation-explanation-reference"},
              {["aria-label"] = "Open explanation for equation " .. number}
            )
          )
          return pandoc.Span({
            link,
            pandoc.Space(),
            pandoc.Str("·"),
            pandoc.Space(),
            explanation,
          })
        end,
      })
    end,
  })

  return notation_linked:walk({
    traverse = "topdown",
    Link = function(link)
      return link, false
    end,
    Str = link_source_markers,
  })
end

return {{Pandoc = number_document}}

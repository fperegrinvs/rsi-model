-- Deterministic global table numbering and cross-page references for Pandoc 3.x.
--
-- Author every substantive table with:
--
--   : Descriptive caption. {#tbl-semantic-id}
--
-- Cite it as `Table [@tbl-semantic-id]`. TABLE_MAP_FILE contains
-- identifier<TAB>number<TAB>output-page and keeps the standalone and
-- multi-page editions on the same main/appendix numbering sequence.

local table_numbers = {}
local table_pages = {}
local seen_tables = {}

local table_map_file = os.getenv("TABLE_MAP_FILE")
if table_map_file == nil or table_map_file == "" then
  error("TABLE_MAP_FILE is required")
end
for line in io.lines(table_map_file) do
  local identifier, number, page = line:match("^([^\t]+)\t([^\t]+)\t?(.*)$")
  if identifier ~= nil then
    table_numbers[identifier] = number
    if page ~= nil and page ~= "" then
      table_pages[identifier] = page
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

local function number_table(tbl)
  if tbl.identifier == "" and os.getenv("QUARTO_SITE_MODE") == "1" then
    -- Quarto's native cross-reference pass moves tbl- identifiers to a
    -- surrounding float Div before user filters run. The post-render site
    -- normalizer applies the global map to that wrapper and its caption.
    return tbl
  end
  if tbl.identifier == "" or not tbl.identifier:match("^tbl%-") then
    error("authored table is missing a semantic tbl- identifier")
  end
  if seen_tables[tbl.identifier] then
    error("duplicate table identifier: " .. tbl.identifier)
  end
  seen_tables[tbl.identifier] = true
  local number = table_numbers[tbl.identifier]
  if number == nil then
    error("table is absent from global map: " .. tbl.identifier)
  end
  if tbl.caption == nil or #tbl.caption.long == 0 then
    error("table is missing a descriptive caption: " .. tbl.identifier)
  end
  tbl.classes:insert("numbered-table")
  tbl.attributes["data-table-number"] = number
  local label = pandoc.Link(
    {pandoc.Str("Table " .. number)},
    "#" .. tbl.identifier,
    "Table " .. number,
    pandoc.Attr(
      "",
      {"table-number"},
      {["aria-label"] = "Table " .. number}
    )
  )
  local first = tbl.caption.long[1]
  if first == nil or (first.t ~= "Plain" and first.t ~= "Para") then
    tbl.caption.long:insert(1, pandoc.Plain({label, pandoc.Str(".")}))
  else
    first.content:insert(1, pandoc.Space())
    first.content:insert(1, pandoc.Str("."))
    first.content:insert(1, label)
  end
  return tbl
end

local function replace_reference(citation)
  if #citation.citations ~= 1 then
    return citation
  end
  local identifier = citation.citations[1].id
  if not identifier:match("^tbl%-") then
    return citation
  end
  local number = table_numbers[identifier]
  if number == nil then
    error("unresolved table reference: " .. identifier)
  end
  return pandoc.Link(
    {pandoc.Str(number)},
    target_for_page(table_pages[identifier] or current_output_page(), identifier),
    "Table " .. number,
    pandoc.Attr(
      "",
      {"table-reference"},
      {["aria-label"] = "Go to table " .. number}
    )
  )
end

local function number_document(document)
  local numbered = document:walk({Table = number_table})
  return numbered:walk({Cite = replace_reference})
end

return {{Pandoc = number_document}}

-- Site-only structural adjustments.
--
-- Quarto's book landing page supplies its own title block from book metadata.
-- The canonical fragment must retain its H1 for Markdown and standalone HTML.
-- Mark that manuscript H1 so the site stylesheet can show it and suppress only
-- the redundant template title block on the landing page.

local site_mode = os.getenv("QUARTO_SITE_MODE") == "1"

function Header(header)
  if site_mode
      and FORMAT:match("html")
      and header.level == 1
      and header.identifier == "recursive-industrial-intelligence" then
    header.classes:insert("publication-title")
    return header
  end
end

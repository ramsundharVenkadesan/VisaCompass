from langchain.tools import tool
from ExecutableTools.SearchTool import tavily_search_invocation

@tool
async def search_ecfr_immigration(query:str) -> str:
    """
    Searches the Electronic Code of Federal Regulations (eCFR) across primary immigration titles.

    Use this tool to discover federal regulations and statutory rules across the three core
    immigration-related titles: Title 8 (Aliens and Nationality - DHS), Title 20 (Employees'
    Benefits - DOL labor certifications), and Title 22 (Foreign Relations - DOS visas).
    Ideal for exploratory regulatory searches when you do not have an exact CFR citation.

    Args:
        query (str): The specific legal concept, visa category, or keyword to search within the regulations (e.g., "H-1B portability", "O-1 extraordinary ability criteria").
    """
    return await tavily_search_invocation(query=f"eCFR Title 8 Title 20 Title 22 {query}", extra_domains=["ecfr.gov"])

@tool
async def get_ecfr_section_text(title:str, part:str, section:str) -> str:
    """
    Retrieves the regulatory text for a specific, known citation in the Electronic Code of Federal Regulations (eCFR).

    Use this tool when you already know the exact CFR citation (Title, Part, and Section)
    and need to read the exact statutory language. For example, to look up 8 CFR 214.2,
    you would pass title="8", part="214", and section="2".

    Args:
        title (str): The eCFR Title number (e.g., "8" for DHS/USCIS, "20" for DOL, "22" for DOS).
        part (str): The part number of the regulation (e.g., "214").
        section (str): The specific section number or sub-section (e.g., "2" or "2(h)").
    """
    return await tavily_search_invocation(query=f"eCFR Title {title} Part {part} Section {section}", extra_domains=["ecfr.gov"])

@tool
async def get_ecfr_title_text(category:str) -> str:
    """
    Searches for USCIS final rules, Federal Register rulemaking, and regulatory background for a specific category.

    Use this tool to find the agency's official regulatory history, policy preambles,
    and final rule announcements rather than just the codified statute. This is helpful
    for understanding the intent, implementation, or recent updates to a specific policy.

    Args:
        category (str): The broad immigration category, policy, or benefit program (e.g., "public charge", "STEM OPT extension", "premium processing fees").
    """
    return await tavily_search_invocation(query=f"USCIS CFR final rule rules and reference for {category}")
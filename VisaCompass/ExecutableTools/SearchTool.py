from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

allowed_domains = ["uscis.gov", "irs.gov", "dol.gov", "dhs.gov",
        "studyinthestates.dhs.gov", "cbp.gov", "travel.state.gov",
        "ecfr.gov", "govinfo.gov", "flag.dol.gov", "flcdatacenter.com",
    ]

tavily_search = TavilySearch(
    max_results=5,
    search_depth='basic',
)

async def get_all_grounded_sources() -> List[Dict[str, str]]:
    official_grounded_sources = {
        "USCIS_EB1_GUIDE": {"title": "USCIS EB-1 Hub",
                            "url": "https://www.uscis.gov/working-in-the-united-states/permanent-workers/employment-based-immigration-first-preference-eb-1",
                            "authority": "USCIS", "citation": "USCIS"},
        "USCIS_EB2_NIW": {"title": "USCIS EB-2 & NIW",
                          "url": "https://www.uscis.gov/working-in-the-united-states/permanent-workers/employment-based-immigration-second-preference-eb-2",
                          "authority": "USCIS", "citation": "USCIS"},
        "DOL_H1B_WHD": {"title": "DOL H-1B Program", "url": "https://www.dol.gov/agencies/whd/immigration/h1b",
                        "authority": "DOL", "citation": "DOL"},
        "IRS_FOREIGN_STUDENTS": {"title": "IRS Foreign Students",
                                 "url": "https://www.irs.gov/individuals/international-taxpayers/foreign-students-scholars-teachers-researchers-and-exchange-visitors",
                                 "authority": "IRS", "citation": "IRS"},
        "USCIS_OPT_GUIDE": {"title": "USCIS OPT Policy",
                            "url": "https://www.uscis.gov/working-in-the-united-states/students-and-exchange-visitors/optional-practical-training-opt-for-f-1-students",
                            "authority": "USCIS", "citation": "USCIS"}
    }
    return list(official_grounded_sources.values())

async def tavily_search_invocation(query:str, extra_domains:List[str]=None) -> str:
    current_domains = list(allowed_domains)
    if extra_domains: current_domains.extend(extra_domains)

    try:
        response = await tavily_search.ainvoke(input={"query":query, "include_domains":current_domains})
        results = response.get('results', [])
        if results:
            formatted_data = [f"Search result for: {query}"]
            for index, result in enumerate(results, start=1):
                title = result.get('title', 'Publication')
                resulting_url = result.get('url', '')
                content = result.get('content', '')
                formatted_data.append(f"[{index}] {title}\nLink:{resulting_url}\nContent:{content.strip()}\n")
            return "\n\n".join(formatted_data)
    except Exception as ex: return f"Error: {str(ex)}"


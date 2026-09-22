#works
import argparse
import asyncio
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# 1. Define a simple schema that gpt-4o-mini can easily output without crashing
class LinkSelection(BaseModel):
    selected_href: str = Field(description="The exact href URL of the chosen link")

async def get_best_link(page, target_concept: str, llm):
    # 2. Extract visible links specifically from the main Wikipedia body
    links = await page.evaluate('''() => {
        return Array.from(document.querySelectorAll('#mw-content-text a[href]'))
            .map(a => ({ text: a.innerText.trim(), href: a.href }))
            .filter(a => a.text.length > 0)
            .slice(0, 200); // Send the first 200 links to keep the context window clean
    }''')
    
    # 3. Format the links into a readable list for the LLM
    links_text = "\n".join([f"Text: '{link['text']}' | Href: {link['href']}" for link in links])
    
    prompt = (
        f"You are an intelligent web navigation assistant.\n"
        f"Your task is to find the best link related to the concept: '{target_concept}'.\n\n"
        f"Available links:\n{links_text}\n\n"
        f"Return ONLY the exact href of the best matching link."
    )
    
    # 4. Use LangChain to force gpt-4o-mini to return ONLY our specific Pydantic schema
    structured_llm = llm.with_structured_output(LinkSelection)
    result = structured_llm.invoke(prompt)
    return result.selected_href

async def wiki_llm_agent(har_name: str):
    # Initialize the mini model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    
    async with async_playwright() as p:
        # Launch Playwright to handle the browser natively
        browser = await p.chromium.launch(headless=False, args=['--disable-web-security'])
        context = await browser.new_context(
            record_har_path=har_name,
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        
        try:
            print("Navigating to Wikipedia...")
            await page.goto("https://en.wikipedia.org/wiki/Artificial_intelligence")
            await page.wait_for_load_state("domcontentloaded")
            
            # Agent Step 1
            print("Asking LLM to find link for 'computational systems'...")
            href_1 = await get_best_link(page, "computational systems", llm)
            print(f"LLM selected: {href_1}")
            await page.goto(href_1)
            await page.wait_for_load_state("domcontentloaded")
            
            # Agent Step 2
            print("Asking LLM to find link for 'machine'...")
            href_2 = await get_best_link(page, "machine", llm)
            print(f"LLM selected: {href_2}")
            await page.goto(href_2)
            await page.wait_for_load_state("domcontentloaded")
            
            # Agent Step 3
            print("Asking LLM to find link for 'thermodynamic system'...")
            href_3 = await get_best_link(page, "thermodynamic system", llm)
            print(f"LLM selected: {href_3}")
            await page.goto(href_3)
            await page.wait_for_load_state("domcontentloaded")
            
            print("Waiting 2 seconds to capture final traffic...")
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await context.close()
            await browser.close()
            print(f"Browser closed. HAR saved to {har_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_name', required=True)
    args = parser.parse_args()
    
    asyncio.run(wiki_llm_agent(args.output_name))
#works
import argparse
import asyncio
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class ElementSelection(BaseModel):
    selected_id: str = Field(description="The exact data-agent-id of the chosen element, or 'NONE' if no matching element is found")

async def get_best_element_and_click(page, target_concept: str, llm):
    # Scrape all visible buttons and links
    elements = await page.evaluate('''() => {
        let items = [];
        let index = 0;
        let nodes = document.querySelectorAll('button, a, [role="button"]');
        
        nodes.forEach(el => {
            let rect = el.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0) {
                let id = 'agent-btn-' + index++;
                el.setAttribute('data-agent-id', id);
                
                let text = el.innerText ? el.innerText.trim().replace(/\\n/g, ' ') : '';
                let aria = el.getAttribute('aria-label') ? el.getAttribute('aria-label').trim() : '';
                
                if (text || aria) {
                    items.push({ id: id, text: text, aria: aria });
                }
            }
        });
        return items;
    }''')
    
    if not elements:
        return False
        
    elements_text = "\n".join([f"ID: {el['id']} | Text: '{el['text']}' | AriaLabel: '{el['aria']}'" for el in elements])
    
    prompt = (
        f"You are an intelligent web navigation assistant.\n"
        f"Your task is to find the UI element that best matches this instruction: '{target_concept}'.\n\n"
        f"Available elements currently on screen:\n{elements_text}\n\n"
        f"Return ONLY the exact ID (e.g., agent-btn-5) of the best matching element. If no element matches the instruction, return 'NONE'."
    )
    
    structured_llm = llm.with_structured_output(ElementSelection)
    result = structured_llm.invoke(prompt)
    
    if result.selected_id == 'NONE':
        print(f"LLM decided: No element found for '{target_concept}'")
        return False
        
    chosen_element = next((el for el in elements if el['id'] == result.selected_id), None)
    selected_name = chosen_element['aria'] if chosen_element and chosen_element['aria'] else (chosen_element['text'] if chosen_element else 'Unknown')
    
    print(f"LLM decided to click -> [ {selected_name} ]")
    
    await page.locator(f"[data-agent-id='{result.selected_id}']").first.click()
    return True

async def soundcloud_llm_agent(har_name: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--disable-web-security'])
        context = await browser.new_context(
            record_har_path=har_name,
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        
        try:
            print("Navigating to SoundCloud...")
            await page.goto("https://on.soundcloud.com/rakZPRfwxJ0xotFC24")
            
            # Wait for page, cookies, and the sign-in modal to load
            await asyncio.sleep(5)
            
            # Step 1: Handle Cookies (if they appear)
            print("Asking LLM to handle cookie banner...")
            await get_best_element_and_click(page, "The button to 'I Accept' or 'Accept cookies'. If no cookie banner is visible, return NONE.", llm)
            await asyncio.sleep(2)
            
            # Step 2: Handle the Sign-In Modal shown in your image
            print("Asking LLM to close the sign-in modal...")
            await get_best_element_and_click(page, "The 'Close' or 'X' button to dismiss the 'Sign in or create an account' popup.", llm)
            await asyncio.sleep(2)
            
            # Step 3: Play the audio
            print("Asking LLM to find the Play button...")
            await get_best_element_and_click(page, "The main 'Play' button for the track.", llm)
            
            print("Agent finished configuration. Waiting 31 seconds to capture traffic...")
            await asyncio.sleep(31)
            
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
    
    asyncio.run(soundcloud_llm_agent(args.output_name))
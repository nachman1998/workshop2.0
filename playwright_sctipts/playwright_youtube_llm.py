#works
import argparse
import asyncio
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class ElementSelection(BaseModel):
    selected_id: str = Field(description="The exact data-agent-id of the chosen element")

async def get_best_element_and_click(page, target_concept: str, llm):
    # Strictly scoped to #movie_player so the LLM ignores the rest of the website
    elements = await page.evaluate('''() => {
        let items = [];
        let index = 0;
        let nodes = document.querySelectorAll('#movie_player button, #movie_player [role="menuitem"], #movie_player [role="menuitemradio"], #movie_player .ytp-menuitem');
        
        nodes.forEach(el => {
            if (el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().height > 0) {
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
    
    elements_text = "\n".join([f"ID: {el['id']} | Text: '{el['text']}' | AriaLabel: '{el['aria']}'" for el in elements])
    
    prompt = (
        f"You are an intelligent web navigation assistant operating a YouTube player.\n"
        f"Your task is to find the UI element that best matches this specific instruction: '{target_concept}'.\n\n"
        f"Available video player elements currently on screen:\n{elements_text}\n\n"
        f"Return ONLY the exact ID (e.g., agent-btn-5) of the best matching element."
    )
    
    structured_llm = llm.with_structured_output(ElementSelection)
    result = structured_llm.invoke(prompt)
    
    chosen_element = next((el for el in elements if el['id'] == result.selected_id), None)
    selected_name = chosen_element['aria'] if chosen_element and chosen_element['aria'] else (chosen_element['text'] if chosen_element else 'Unknown')
    
    print(f"LLM decided to click -> [ {selected_name} ]")
    
    await page.locator(f"[data-agent-id='{result.selected_id}']").first.click()

async def youtube_llm_agent(har_name: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=['--disable-web-security'])
        context = await browser.new_context(
            record_har_path=har_name,
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        
        try:
            print("Navigating to YouTube...")
            await page.goto("https://www.youtube.com/watch?v=7bOptq-NPJQ")
            
            await asyncio.sleep(5)
            try:
                await page.get_by_role("button", name="Accept all").click(timeout=2000)
            except:
                pass
                
            print("Waking up video player controls...")
            await page.locator('#movie_player').hover()
            await asyncio.sleep(1)
            
            # Step 1: Explicitly target the gear icon
            print("Locating Settings gear icon...")
            await get_best_element_and_click(page, "The Settings gear icon. Usually has aria-label 'Settings'.", llm)
            await asyncio.sleep(2.5) 
            
            # Step 2: Forbid it from clicking the gear icon again
            print("Locating Quality menu item...")
            await get_best_element_and_click(page, "The menu item containing the word 'Quality'. CRITICAL: Do NOT select the Settings gear icon again.", llm)
            await asyncio.sleep(2.5) 
            
            # Step 3: Lock onto 1080p
            print("Locating 1080p resolution option...")
            await get_best_element_and_click(page, "The menu option containing '1080p'.", llm)

            print("Step 4: Checking if the video is currently playing...")
            # Evaluate the underlying HTML5 video element's paused state
            is_paused = await page.evaluate("() => { const v = document.querySelector('video'); return v ? v.paused : false; }")
            
            if is_paused:
                print("Video was paused. Resuming playback...")
                # Press 'k', which is YouTube's universal shortcut to toggle Play/Pause
                await page.keyboard.press("k")
            else:
                print("Video is already playing smoothly.")
            
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
    
    asyncio.run(youtube_llm_agent(args.output_name))
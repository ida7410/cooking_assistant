import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


class RecipeSimplifier:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-20250514"


    def simplify(self, recipe_name, steps, difficulty="Easy"):
        if isinstance(steps, list):
            steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        else:
            steps_text = str(steps)

        prompt = f"""You are a patient cooking instructor helping complete beginners make: {recipe_name}

Rewrite these recipe steps in very simple, beginner-friendly language following these rules:

1. REPLACE JARGON with simple words:
   - "Julienne" → "Cut into thin strips"
   - "Sauté" → "Cook in pan while stirring"
   - "Deglaze" → "Add liquid and scrape the bottom"
   - "Fold" → "Gently mix by turning over"
   - "Simmer" → "Cook on low heat with small bubbles"

2. BE SPECIFIC with measurements and times:
   - "Heat until shimmering" → "Heat for 2 minutes on medium-high"
   - "Cook until done" → "Cook for 5-7 minutes until golden brown"
   - "Add oil" → "Add 2 tablespoons of oil"

3. DESCRIBE what to look for:
   - "Until fragrant" → "Until you can smell it (about 1-2 minutes)"
   - "Until translucent" → "Until you can see through it (looks see-through)"
   - "Until golden" → "Until it turns light brown color"

4. BREAK DOWN complex steps:
   - If a step has multiple actions, split it into separate numbered steps

5. ADD HELPFUL TIPS:
   - Mention when to stir, what temperature to use, how it should look/smell

Original recipe steps:
{steps_text}

Now write the simplified beginner-friendly version. Use numbered steps:"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            simplified = message.content[0].text.strip()
            return simplified
        except Exception as e:
            print(f"Exception while simplifying recipe: {e}")
            print(steps_text)


def main():
    simplifier = RecipeSimplifier()
    import pandas as pd
    df = pd.read_csv('data/RAW_recipes.csv')

    # Find a recipe with interesting steps
    recipe = df[df['name'].str.contains('fried rice', case=False, na=False)].iloc[0]

    print(recipe['steps'])
    simplified = simplifier.simplify(
        recipe_name=recipe['name'],
        steps=recipe['steps']
    )
    print(simplified)

if __name__ == "__main__":
    main()
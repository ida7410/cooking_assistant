// This is like a blueprint/contract
export interface Recipe {
  id: number;
  name: string;
  match_percentage: number;
  cooking_time: number;
  difficulty: string;
  missing_ingredients: string[];
}

export interface RecipeSearchResponse {
  recipes: Recipe[];
  total_results: number;
}
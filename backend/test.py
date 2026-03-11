"""
Test all recommenders before deployment
"""
from models.recommender_manager import get_recommender_manager
from schemas.recipe import Recipe

print("=" * 80)
print("🧪 TESTING ALL RECOMMENDERS")
print("=" * 80)

# Initialize manager (loads data once)
print("\n1. Initializing Recommender Manager...")
manager = get_recommender_manager()
print("✅ Manager initialized\n")

# Get a test recipe from the dataset
print("2. Loading test recipe...")
test_recipe_row = manager.recipes[manager.recipes['name'].str.contains('banana bread', case=False, na=False)].iloc[0]
test_recipe = Recipe.get_recipe_dataframe_from_row(test_recipe_row)
print(f"✅ Test recipe: {test_recipe.name} (ID: {test_recipe.id})\n")

# Test Content Recommender
print("=" * 80)
print("3. Testing Content Recommender...")
print("=" * 80)
try:
    content_rec = manager.get_content_recommender()
    content_result = content_rec.find_similar(test_recipe, top_n=5)

    print(f"Status: {content_result.status}")
    print(f"Strategy: {content_result.strategy}")
    print(f"Found {len(content_result.recommendations)} recommendations")

    if content_result.status == 'success':
        print("\nTop 3 recommendations:")
        for i, rec in enumerate(content_result.recommendations[:3], 1):
            print(f"  {i}. {rec.recipe.name}")
            print(f"     Similarity: {rec.similarity_score:.3f}")
            print(f"     Ingredients: {rec.ingredient_similarity:.3f}")
            print(f"     Tags: {rec.tag_similarity:.3f}")
        print("✅ Content recommender works!\n")
    else:
        print(f"❌ Error: {content_result.error_message}\n")
except Exception as e:
    print(f"❌ Content recommender failed: {e}\n")

# Test Collaborative Recommender
print("=" * 80)
print("4. Testing Collaborative Recommender...")
print("=" * 80)
try:
    collab_rec = manager.get_collab_recommender()
    collab_result = collab_rec.find_similar(test_recipe, top_n=5)

    print(f"Status: {collab_result.status}")
    print(f"Strategy: {collab_result.strategy}")

    if collab_result.status == 'success':
        print(f"Found {len(collab_result.recommendations)} recommendations")
        print("\nTop 3 recommendations:")
        for i, rec in enumerate(collab_result.recommendations[:3], 1):
            print(f"  {i}. {rec.recipe.name}")
            print(f"     Similarity: {rec.similarity_score:.3f}")
            print(f"     Common users: {rec.common_users}")
        print("✅ Collaborative recommender works!\n")
    else:
        print(f"⚠️  Error: {collab_result.error_message}")
        print("   (This is expected if recipe has few ratings)\n")
except Exception as e:
    print(f"❌ Collaborative recommender failed: {e}\n")

# Test Hybrid Recommender
print("=" * 80)
print("5. Testing Hybrid Recommender...")
print("=" * 80)
try:
    hybrid_rec = manager.get_hybrid_recommender()
    hybrid_result = hybrid_rec.find_similar(test_recipe, top_n=5)

    print(f"Status: {hybrid_result.status}")
    print(f"Strategy: {hybrid_result.strategy}")
    print(f"Found {len(hybrid_result.recommendations)} recommendations")

    if hybrid_result.status == 'success':
        print("\nTop 3 recommendations:")
        for i, rec in enumerate(hybrid_result.recommendations[:3], 1):
            print(f"  {i}. {rec.recipe.name}")
            print(f"     Hybrid score: {rec.similarity_score:.3f}")
            print(f"     Content: {rec.content_score:.3f} | Collab: {rec.collab_score:.3f}")
            if rec.in_both:
                print(f"     ⭐ Found in BOTH recommenders!")
        print("✅ Hybrid recommender works!\n")
    else:
        print(f"❌ Error: {hybrid_result.error_message}\n")
except Exception as e:
    print(f"❌ Hybrid recommender failed: {e}\n")

# Test Recipe Matcher
print("=" * 80)
print("6. Testing Recipe Matcher...")
print("=" * 80)
try:
    from models.recipe_matcher import RecipeMatcher

    matcher = RecipeMatcher()
    test_ingredients = ['chicken', 'rice', 'soy sauce']

    match_result = matcher.find_matches(test_ingredients, top_n=3)

    print(f"Status: {match_result.status}")
    print(f"Strategy: {match_result.strategy}")
    print(f"Found {len(match_result.recommendations)} matches")

    if match_result.status == 'success':
        print(f"\nMatches for ingredients: {test_ingredients}")
        for i, rec in enumerate(match_result.recommendations, 1):
            print(f"  {i}. {rec.recipe.name}")
            print(f"     Match: {rec.similarity_score:.3f}")
        print("✅ Recipe matcher works!\n")
except Exception as e:
    print(f"❌ Recipe matcher failed: {e}\n")

print("=" * 80)
print("🎉 ALL TESTS COMPLETE!")
print("=" * 80)
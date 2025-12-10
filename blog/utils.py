def map_category_to_byline(target_category):
    """
    Maps NewsVoir categories → Your site's categories.
    You will customize this mapping.
    """
    from blog.models import Category

    mapping = {
        "Economy": "Economy",
        "Technology": "Technology",
        "Sports": "Sports",
        "Business": "Business",
        "Finance": "Finance",
        "Entertainment" : "Entertainment",
        "Politics" : "Politics",
        "Real Estate" : "Real Estate",
        "Aviation" : "Aviation",
        "Defense" : "Defense",
        "Fintech" : "Fintech",
        "Automobiles" : "Automobiles",
        "Stock Market" : "Stock Market",
        "Space" : "Space",
        "Startups" : "Startups",
        "AI" : "AI",
        "Policy" : "Policy",
        "Corporate" : "Corporate",
        "Cyber Security" : "Cyber Security",
        "Social Media" : "Social Media",
        
        
        # add more here
    }

    byline_cat = mapping.get(target_category)
    if not byline_cat:
        return None

    return Category.objects.filter(name__iexact=byline_cat).first()

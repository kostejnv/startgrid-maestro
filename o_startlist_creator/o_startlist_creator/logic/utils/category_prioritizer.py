import re

# from o_startlist_creator.logic.category import Category

class CategoryPrioritizer:
    def __init__(self, categories):
        self.categories = categories
        self.young_cat_coefs, self.old_cat_coefs = (-100/11,2100/11), (100/59,-2100/59)
        self.prioritize()
        
    def prioritize(self):
        sorted_cats = sorted(list(self.categories.keys()), key=self.sort_criterium)
        self.priorities = {cat: i for i, cat in enumerate(sorted_cats)}
        
    def get_priority(self):
        return [self.priorities[cat] for cat in self.categories]
        
        
    def sort_criterium(self, cat):
        match_age = re.search(r'\d+', cat)
        if match_age and 10 <= int(match_age.group()) <= 80:
            category_age = int(match_age.group())
            a,b = self.young_cat_coefs if category_age < 21 else self.old_cat_coefs
            return a*category_age + b
        else:
            return 50
        
if __name__ == '__main__':
    cats_name = ["D10", "D10L", "D12", "D12D", "D14", "D14D", "D16", "D18", "D20", "D21K", "D21L", "D35", "D40", "D45", "D50", "D55", "D60", "D65", "D70", "D75", "H10", "H10L", "H12", "H12D", "H14", "H14D", "H16", "H18", "H20", "H21K", "H21L", "H35", "H40", "H45", "H50", "H55", "H60", "H65", "H70", "H75", "H80", "HDR", "P", "T"]
    cats = {name:0 for name in cats_name}
    priorities = CategoryPrioritizer(cats).get_priority()
    for cat, priority in zip(cats_name, priorities):
        print(cat, priority)
    
    
    
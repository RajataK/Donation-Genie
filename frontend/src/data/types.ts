export interface FoodBank {
  id: string;
  name: string;
  distance: string;
  distanceMiles: number;
  urgencyStatus: "urgent" | "active";
  familiesServed: number;
  topNeeds: string[];
  impactStory: string;
}

export interface WishListItem {
  id: string;
  name: string;
  description: string;
  urgencyLevel: "urgent" | "needed";
  category: string;
  estimatedPrice: number;
}

export interface RecipeIngredient {
  name: string;
  matched: boolean;
}

export interface RecipeKit {
  id: string;
  name: string;
  icon: string;
  servings: string;
  prepTime: string;
  ingredients: RecipeIngredient[];
  totalCost: number;
}

export interface BasketItem {
  id: string;
  name: string;
  quantity: number;
  unitPrice: number;
}

export interface DonationBasket {
  foodBankId: string;
  foodBankName: string;
  items: BasketItem[];
  deliveryCost: number;
  totalCost: number;
  donationType: "direct" | "recipe-kit";
  recipeName: string | null;
}

export interface SupermarketProduct {
  name: string;
  retailer: string;
  price: number;
}

export interface QRCodeFormat {
  id: string;
  label: string;
  description: string;
  fileType: string;
}

export interface DeliveryPreference {
  id: string;
  label: string;
  description: string;
  enabled: boolean;
}

export interface SupermarketPartner {
  id: string;
  name: string;
  deliveryTime: string;
  available: boolean;
  enabled: boolean;
}

import type {
  FoodBank,
  WishListItem,
  RecipeKit,
  SupermarketProduct,
  QRCodeFormat,
  DeliveryPreference,
  SupermarketPartner,
} from "./types";

export const foodBanks: FoodBank[] = [
  {
    id: "camden-food-bank",
    name: "Camden Community Food Bank",
    distance: "0.8 miles away",
    distanceMiles: 0.8,
    urgencyStatus: "urgent",
    familiesServed: 150,
    topNeeds: ["Tinned Tomatoes", "Pasta", "Rice", "Cooking Oil"],
    impactStory:
      "Last month, Camden Community Food Bank provided emergency food parcels to 150 families in the local area. Your donations directly help stock their shelves with essential items that families need most.",
  },
  {
    id: "islington-food-aid",
    name: "Islington Food Aid",
    distance: "1.2 miles away",
    distanceMiles: 1.2,
    urgencyStatus: "active",
    familiesServed: 89,
    topNeeds: ["Cereal", "UHT Milk", "Tinned Soup", "Tea"],
    impactStory:
      "Islington Food Aid supports 89 families weekly with nutritious food parcels. They work closely with local schools to identify families in need and ensure children have access to regular meals.",
  },
  {
    id: "kings-cross-pantry",
    name: "King's Cross Community Pantry",
    distance: "2.1 miles away",
    distanceMiles: 2.1,
    urgencyStatus: "active",
    familiesServed: 62,
    topNeeds: ["Baked Beans", "Tinned Fruit", "Biscuits", "Juice"],
    impactStory:
      "King's Cross Community Pantry operates on a membership model, giving families dignity and choice in selecting their weekly groceries. Your donations help keep their shelves stocked with variety.",
  },
];

export const wishListItems: WishListItem[] = [
  {
    id: "tinned-tomatoes",
    name: "Tinned Tomatoes",
    description: "400g tins — essential for family meals",
    urgencyLevel: "urgent",
    category: "Tinned Goods",
    estimatedPrice: 0.85,
  },
  {
    id: "pasta",
    name: "Pasta",
    description: "500g bags of dried pasta",
    urgencyLevel: "urgent",
    category: "Dry Goods",
    estimatedPrice: 1.2,
  },
  {
    id: "rice",
    name: "Rice",
    description: "1kg bags of long grain rice",
    urgencyLevel: "needed",
    category: "Dry Goods",
    estimatedPrice: 1.5,
  },
  {
    id: "cooking-oil",
    name: "Cooking Oil",
    description: "1 litre vegetable or sunflower oil",
    urgencyLevel: "urgent",
    category: "Cooking Essentials",
    estimatedPrice: 2.0,
  },
  {
    id: "uht-milk",
    name: "UHT Milk",
    description: "1 litre semi-skimmed",
    urgencyLevel: "needed",
    category: "Dairy",
    estimatedPrice: 1.1,
  },
  {
    id: "tinned-soup",
    name: "Tinned Soup",
    description: "400g tins — variety of flavours",
    urgencyLevel: "needed",
    category: "Tinned Goods",
    estimatedPrice: 0.95,
  },
];

export const recipeKits: RecipeKit[] = [
  {
    id: "spaghetti-bolognese",
    name: "Spaghetti Bolognese Kit",
    icon: "\ud83c\udf5d",
    servings: "Feeds family of 4",
    prepTime: "Ready in 30 mins",
    ingredients: [
      { name: "Pasta (500g)", matched: true },
      { name: "Tinned Tomatoes (2x 400g)", matched: true },
      { name: "Cooking Oil (250ml)", matched: true },
      { name: "Onion (1)", matched: false },
      { name: "Garlic (1 bulb)", matched: false },
    ],
    totalCost: 5.8,
  },
  {
    id: "vegetable-soup",
    name: "Hearty Vegetable Soup Kit",
    icon: "\ud83c\udf72",
    servings: "Feeds family of 4",
    prepTime: "Ready in 45 mins",
    ingredients: [
      { name: "Tinned Tomatoes (400g)", matched: true },
      { name: "Rice (250g)", matched: true },
      { name: "Tinned Soup Base (400g)", matched: true },
      { name: "Mixed Vegetables (tin)", matched: false },
    ],
    totalCost: 4.5,
  },
  {
    id: "rice-curry",
    name: "Simple Rice & Curry Kit",
    icon: "\ud83c\udf5b",
    servings: "Feeds family of 4",
    prepTime: "Ready in 35 mins",
    ingredients: [
      { name: "Rice (1kg)", matched: true },
      { name: "Cooking Oil (250ml)", matched: true },
      { name: "Tinned Tomatoes (400g)", matched: true },
      { name: "Curry Paste (jar)", matched: false },
      { name: "UHT Milk (500ml)", matched: true },
    ],
    totalCost: 6.2,
  },
];

export const supermarketProducts: SupermarketProduct[] = [
  { name: "Tesco Chopped Tomatoes 400g", retailer: "Tesco", price: 0.45 },
  {
    name: "Tesco Penne Pasta 500g",
    retailer: "Tesco",
    price: 0.7,
  },
  {
    name: "Tesco Vegetable Oil 1L",
    retailer: "Tesco",
    price: 1.65,
  },
  {
    name: "Tesco Long Grain Rice 1kg",
    retailer: "Tesco",
    price: 1.2,
  },
  {
    name: "Tesco UHT Semi-Skimmed Milk 1L",
    retailer: "Tesco",
    price: 0.85,
  },
];

export const qrCodeFormats: QRCodeFormat[] = [
  {
    id: "poster",
    label: "In-Store Poster",
    description: "A4 poster with QR code and donation info",
    fileType: "PDF",
  },
  {
    id: "sticker",
    label: "Sticker / Label",
    description: "Small label for shelf or counter display",
    fileType: "PNG",
  },
  {
    id: "social",
    label: "Social Media",
    description: "Square format for social media posts",
    fileType: "JPG",
  },
];

export const deliveryPreferences: DeliveryPreference[] = [
  {
    id: "direct-delivery",
    label: "Direct Delivery",
    description:
      "Items delivered directly to the food bank from the supermarket",
    enabled: true,
  },
  {
    id: "donor-collection",
    label: "Donor Collection",
    description: "Donor collects items and delivers in person",
    enabled: false,
  },
];

export const supermarketPartners: SupermarketPartner[] = [
  {
    id: "tesco",
    name: "Tesco",
    deliveryTime: "Next day delivery",
    available: true,
    enabled: true,
  },
  {
    id: "sainsburys",
    name: "Sainsbury's",
    deliveryTime: "2-3 day delivery",
    available: true,
    enabled: false,
  },
  {
    id: "asda",
    name: "Asda",
    deliveryTime: "Coming soon",
    available: false,
    enabled: false,
  },
];

export const aiSummaryText =
  "Based on 3 food banks near SW1A 1AA, the most urgent needs are tinned goods (tomatoes, soup), dry staples (pasta, rice), and cooking essentials (oil, UHT milk). Camden Community Food Bank has the highest urgency level.";

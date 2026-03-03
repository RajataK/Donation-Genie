import dotenv from "dotenv";
import fs from "fs";

dotenv.config({ path: ".env" });
const PEPESTO_KEY = process.env.PEPESTO_KEY;
const TARGET_SUPERMARKET_DOMAIN = "tesco.com";

const ROOT_URL = "https://s.pepesto.com/api";
const BEARER = `Bearer ${PEPESTO_KEY}`;

const MOCK_RECIPES = {
  recipes: [
    {
      title: "Crispy Potato Salad with Creamy Yogurt Dill Dressing",
      ingredients: [
        "1 lemon",
        "700g potatoes (~3)",
        "30g red onions",
        "30g spring onions",
        "parsley",
        "dill",
        "120ml yogurt",
        "1tsp baking soda",
        "olive oil",
        "apple vinegar",
        "2tsp black pepper",
        "smoked paprika",
        "garlic powder",
        "1tsp salt",
        "mayonnaise",
      ],
      steps: [
        "Boil halved baby potatoes with salt and pepper until fork-tender.",
        "Preheat oven to 221°F.",
        "Drain and season potatoes with olive oil, salt, pepper, garlic powder, and smoked paprika.",
        "Roast seasoned potatoes for about 20 minutes.",
        "Prepare the dressing by mixing Greek yogurt, mayonnaise, lemon juice and zest, dill, parsley, apple cider vinegar, salt, and pepper.",
        "Pour the dressing over slightly cooled roasted potatoes.",
        "Top with red onions, green onions, dill, and smoky chili flakes.",
      ],
      image_url:
        "https://storage.googleapis.com/pepesto_recipe_images/9b0eea847bebd59141b9615a5b.webp",
      nutrition: {
        calories: 1908,
        carbohydrates_grams: 127,
        protein_grams: 16,
        fat_grams: 141,
      },
      kg_token:
        "EjYKNENyaXNweSBQb3RhdG8gU2FsYWQgd2l0aCBDcmVhbXkgWW9ndXJ0IERpbGwgRHJlc3NpbmdKLSIHMSBsZW1vbjIXCOy5oN8EIA8yBkxlbW9uc1ACXQAAcEE4nP//////////AUo/IhI3MDBnIHBvdGF0b2VzICh+MykyHgiv34DEt/q3+QsgqAUyCFBvdGF0b2VzUAFdAAAqRDid//////////8BSjwiDjMwZyByZWQgb25pb25zMh8I3pqowrqT3OlGIB4yClJlZCBvbmlvbnNQAl0AAPBBOJ3//////////wFKPiIRMzBnIHNwcmluZyBvbmlvbnMyHgjXuLzUCSAeMg1TcHJpbmcgb25pb25zUAFdAADwQTid//////////8BSjIiB3BhcnNsZXkyHAiz2pCOo/b8mTogBTIHUGFyc2xleVACXQAAoEA4nv//////////AUosIgRkaWxsMhkI/bPStPvT45dHIAUyBERpbGxQAl0AAKBAOJ7//////////wFKMiIMMTIwbWwgeW9ndXJ0MhcItMGLlQ4geDIGWW9ndXJ0UAJdAADwQjin//////////8BSj8iEDF0c3AgYmFraW5nIHNvZGEyIAiwsICwhbeymjMgATILQmFraW5nIFNvZGFQB10AAAA/OLv//////////wFKOCIJb2xpdmUgb2lsMiAI5KqRksv5yp4GGAEgLTIJT2xpdmUgb2lsUAJdAAA0QjjE//////////8BSkAiDWFwcGxlIHZpbmVnYXIyJAj0np26mpjBzF0YASAFMg1BcHBsZSB2aW5lZ2FyUAddAACAPzjH//////////8BSkIiETJ0c3AgYmxhY2sgcGVwcGVyMiII+f/rwK/wtQcYASAGMgxCbGFjayBwZXBwZXJQB10AAABAOMj//////////wFKQiIOc21va2VkIHBhcHJpa2EyJQiT5eWC1fLnr04YASABMg5TbW9rZWQgcGFwcmlrYVAHXQAAAD84yP//////////AUpAIg1nYXJsaWMgcG93ZGVyMiQI7enp/Mj7o48MGAEgATINR2FybGljIHBvd2RlclAHXQAAAD84yP//////////AUozIgkxdHNwIHNhbHQyGwiYqvD3geDjizsYASAEMgRTYWx0UAddAADAPzjI//////////8BSjYiCm1heW9ubmFpc2UyHQidsce1AxgBIHgyCk1heW9ubmFpc2VQAl0AAPBCOMr//////////wE=",
    },
    {
      title: "BBQ Bacon-Wrapped Mozzarella Sticks",
      ingredients: [
        "2 eggs",
        "300g mozzarella cheese",
        "250g bacon",
        "flour",
        "100g breadcrumbs",
        "sunflower oil",
        "garlic powder",
        "paprika powder",
        "salt",
        "black pepper",
      ],
      steps: [
        "Wrap each mozzarella stick with a slice of bacon and secure with toothpicks.",
        "Whisk the eggs in one bowl.",
        "Mix breadcrumbs, flour, garlic powder, paprika, salt, and pepper in another bowl.",
        "Dip each bacon-wrapped mozzarella stick into the egg, then coat with the breadcrumb mixture. Repeat for a thicker crust.",
        "Heat cooking oil in a deep pan over medium heat.",
        "Fry the coated sticks for 2–3 minutes per side until golden brown and crispy. Transfer to a paper towel to drain excess oil.",
        "Alternatively, preheat oven to 200°C. Place sticks on a baking sheet lined with parchment paper. Bake for 15–20 minutes, flipping halfway through.",
        "Serve warm with marinara sauce, ranch dressing, or BBQ sauce for dipping.",
      ],
      image_url:
        "https://storage.googleapis.com/pepesto_recipe_images/425fe1a1749f49cbdfd0ffbdf2.webp",
      nutrition: {
        calories: 3018,
        carbohydrates_grams: 122,
        protein_grams: 148,
        fat_grams: 209,
      },
      kg_token:
        "EiUKI0JCUSBCYWNvbi1XcmFwcGVkIE1venphcmVsbGEgU3RpY2tzSiwiBjIgZWdnczIXCLi4iYYHIGQoAjIERWdnc1ADXQAAAEA4pv//////////AUpMIhYzMDBnIG1venphcmVsbGEgY2hlZXNlMicI/5T+r+ChwKdFIKwCMhFNb3p6YXJlbGxhIGNoZWVzZVABXQAAlkM4p///////////AUo0IgoyNTBnIGJhY29uMhsI+sjK5PuB3b1IIPABMgVCYWNvblABXQAAcEM4s///////////AUowIgVmbG91cjIcCIeB77fC+szpOBgBIDwyBUZsb3VyUAFdAABwQji6//////////8BSjsiEDEwMGcgYnJlYWRjcnVtYnMyHAiUv76iByBkMgtCcmVhZGNydW1ic1ABXQAAyEI4u///////////AUpAIg1zdW5mbG93ZXIgb2lsMiQIo7nss8znrbIZGAEgDzINU3VuZmxvd2VyIG9pbFACXQAAcEE4xP//////////AUpAIg1nYXJsaWMgcG93ZGVyMiQI7enp/Mj7o48MGAEgATINR2FybGljIHBvd2RlclAHXQAAAD84yP//////////AUpCIg5wYXByaWthIHBvd2RlcjIlCMO3yozV+MCYNRgBIAEyDlBhcHJpa2EgcG93ZGVyUAddAAAAPzjI//////////8BSi4iBHNhbHQyGwiYqvD3geDjizsYASABMgRTYWx0UAldAACAPzjI//////////8BSj0iDGJsYWNrIHBlcHBlcjIiCPn/68Cv8LUHGAEgATIMQmxhY2sgcGVwcGVyUAldAACAPzjI//////////8B",
    },
    {
      title: "Baked Cod with Mussel Sauce",
      ingredients: [
        "2 garlic cloves",
        "70g onions",
        "60g carrots",
        "30ml tomato paste",
        "500g canned tomatoes",
        "parsley",
        "700g cod fish",
        "350g mussels",
        "sugar",
        "olive oil",
        "1tsp black pepper",
        "1tsp salt",
        "fish broth",
      ],
      steps: [
        "Preheat oven to 175°C (350°F).",
        "Season cod fillets with salt and pepper, and place in a greased ovenproof dish.",
        "Bake in the oven for about 20 minutes.",
        "For the mussel sauce, finely chop the garlic, onion, and carrot.",
        "Roughly pound the fennel seeds in a mortar and pestle.",
        "Sauté the garlic, onion, carrot, and fennel seeds in olive oil in a saucepan until softened.",
        "Stir in the tomato paste and cook for 1 minute.",
        "Add the crushed tomatoes, fish stock, and water or wine. Simmer for about 10 minutes without a lid.",
        "Drain the mussels, reserving some of the liquid, and add them to the sauce along with the parsley.",
        "Season with sugar, salt, and pepper.",
        "Serve the mussel sauce over the baked cod, with roasted potato halves and lightly cooked vegetables.",
      ],
      image_url:
        "https://storage.googleapis.com/pepesto_recipe_images/bec5fd1e25e9fa354e57e8fdee.webp",
      nutrition: {
        calories: 1323,
        carbohydrates_grams: 50,
        protein_grams: 186,
        fat_grams: 32,
      },
      kg_token:
        "Eh0KG0Jha2VkIENvZCB3aXRoIE11c3NlbCBTYXVjZUo1Ig8yIGdhcmxpYyBjbG92ZXMyFwiZzNPVCCAGMgZHYXJsaWNQCl0AAABAOJ3//////////wFKMCIKNzBnIG9uaW9uczIXCJaVuYwCIEYyBk9uaW9uc1ABXQAAjEI4nf//////////AUo2Igs2MGcgY2Fycm90czIcCIyhr6GRjNLrbiA8MgdDYXJyb3RzUAFdAABwQjid//////////8BSkEiETMwbWwgdG9tYXRvIHBhc3RlMiEItMDlj7CjgeR7IB4yDFRvbWF0byBwYXN0ZVACXQAA8EE4nf//////////AUpIIhQ1MDBnIGNhbm5lZCB0b21hdG9lczIlCLmrkqLtgNrSPiD0AzIPQ2FubmVkIHRvbWF0b2VzUAFdAAD6Qzid//////////8BSjIiB3BhcnNsZXkyHAiz2pCOo/b8mTogDzIHUGFyc2xleVACXQAAcEE4nv//////////AUo2Ig03MDBnIGNvZCBmaXNoMhoI6bDX0gwgvAUyCENvZCBmaXNoUAFdAAAvRDiw//////////8BSjgiDDM1MGcgbXVzc2VsczIdCMPJqPvlzu3bDiDoAjIHTXVzc2Vsc1ABXQAAtEM4sf//////////AUowIgVzdWdhcjIcCK2yub/ktce3cBgBIAEyBVN1Z2FyUAddAAAAPzi7//////////8BSjgiCW9saXZlIG9pbDIgCOSqkZLL+cqeBhgBIB4yCU9saXZlIG9pbFACXQAA8EE4xP//////////AUpCIhExdHNwIGJsYWNrIHBlcHBlcjIiCPn/68Cv8LUHGAEgAjIMQmxhY2sgcGVwcGVyUAddzczMPjjI//////////8BSjMiCTF0c3Agc2FsdDIbCJiq8PeB4OOLOxgBIAMyBFNhbHRQB10AAKA/OMj//////////wFKOCIKZmlzaCBicm90aDIfCJ3X/KELGAEgASgBMgpGaXNoIGJyb3RoUANdAACAPzjJ//////////8B",
    },
  ],
};

const MOCK_PRODUCTS = {
  items: [
    {
      item_name: "Cherry tomatoes",
      products: [
        {
          product: {
            product_name: "Nightingale Farms Cherry Tomatoes",
            quantity: { grams: 250 },
            price: { price: 62, promotion: { promo: true } },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/292213267",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/50ae2616-9ae0-4e5f-8457-1cfadecf9eed/86de7558-faca-4286-a294-830fea0b4802_1001944737.jpeg",
            classification: {},
          },
          num_units_to_buy: 2,
        },
        {
          product: {
            product_name: "Tesco Baby Plum Tomatoes 300G",
            quantity: { grams: 300 },
            price: { price: 90, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/314119392",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/ff7c695d-ef54-40f4-96f3-9323eb5b2577/9c5e7890-2d06-4724-9ad6-195ba2c24c42.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Cherry Tomatoes 300G",
            quantity: { grams: 300 },
            price: { price: 100, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/313968087",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/d01ebea0-8dc5-4f6d-b0a9-272f6d48798d/11ef3b1c-8894-4869-bce8-66b35025ddc5.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Azura Sun Joy Baby Plum Tomatoes",
            quantity: { grams: 250 },
            price: { price: 130, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/322842847",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/b5032d43-0913-4234-9203-3e32fd7c02a9/fc8a4e70-c838-4f68-a617-53248eb5b5b6.jpeg",
            classification: {},
          },
          num_units_to_buy: 2,
        },
        {
          product: {
            product_name: "Tesco Finest Baby Tomatoes on the Vine 400g",
            quantity: { grams: 400 },
            price: { price: 330, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/317209442",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/6bc31ef1-f825-4db0-8141-5c253f3fb7d8/c0fe9f42-24c4-4799-b18e-ab5d36504b3e.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Organic Cherry Tomatoes On The Vine 200g",
            quantity: { grams: 200 },
            price: { price: 209, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/265555588",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/8a7eced3-9632-42b7-bce8-ea28dcf0aa70/54b24bc3-5562-4d20-b667-db18c0ac1462.jpeg",
            classification: { is_bio: true },
          },
          num_units_to_buy: 2,
        },
        {
          product: {
            product_name: "Tesco Finest Piccobella Tomatoes 220G",
            quantity: { grams: 220 },
            price: { price: 209, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/308091212",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/50a775b3-2099-4006-902d-81ea555dff3a/db3beada-6a51-465f-9883-9490a439edc4.jpeg",
            classification: {},
          },
          num_units_to_buy: 2,
        },
      ],
    },
    {
      item_name: "Butter",
      products: [
        {
          product: {
            product_name: "Clover Original Spread 500g",
            quantity: { grams: 500 },
            price: {
              price: 175,
              promotion: { promo: true, promo_percentage: 32 },
            },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/254263685",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/49323584-0897-4c65-8b69-db505fd688c8/5fa1089e-e171-438f-8353-35bc4c9ca9db_1123051072.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco British Salted Spreadable",
            quantity: { grams: 500 },
            price: { price: 199, promotion: { promo: true } },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/291725665",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/1d53202a-c601-40a6-b3c9-45b166f42801/6d05e504-b775-45ef-90f6-ff3a9c88f5bb.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Crisp N' Dry Solid Block 250G",
            quantity: { grams: 250 },
            price: { price: 100, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/288354192",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/8f6cacda-028e-4ce0-949a-769b582e80fb/3afba73a-5d88-421f-a79f-74ed6507edd6.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Yeo Valley Organic Salted Butter 200g",
            quantity: { grams: 200 },
            price: { price: 310, promotion: { promo: true } },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/314313213",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/9233f2f4-b68e-4e55-933f-0c020a4bde4a/2a0b2c44-65b5-42c5-8af6-12e1d29470ee_1990357945.jpeg",
            classification: { is_bio: true },
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Lurpak Unsalted Butter 200G",
            quantity: { grams: 200 },
            price: { price: 280, promotion: { promo: true } },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/314414883",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/4f797ac3-5d45-44c9-a79f-62b5d0c1ed59/1a86df25-ed3b-48f6-a2a2-d648be34a5ea_1624599483.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Vitalite Dairy Free Spread 500G",
            quantity: { grams: 500 },
            price: { price: 155, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/253250771",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/c3a69ba1-e97d-4348-a731-aae2ebf76165/20df294c-688a-4661-9b00-80289465d5e8.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Pure Dairy Free Buttery Spread 500G",
            quantity: { grams: 500 },
            price: { price: 215, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/305971345",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/2a9d9ee5-2e9f-4aa8-880e-6a9b21c23d4a/dbac28d4-3085-4c65-96f6-6a4ab4fc75f3_594588583.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Reduced Fat Butterpak Spreadable 500G",
            quantity: { grams: 500 },
            price: { price: 218, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/291725826",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/f9db224a-e0f3-41d9-a3c6-9e90102b5889/f414699d-b7b2-42bc-86f4-1dee8e98b23c.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Organic Salted Butter 250G",
            quantity: { grams: 250 },
            price: { price: 320, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/253114455",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/b51c3fb7-b08b-46b7-95ec-2b0446a3bcb3/df7bffda-4e82-4bc8-8c7e-8babaa6b8952.jpeg",
            classification: { is_bio: true },
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Organic Unsalted Butter 250G",
            quantity: { grams: 250 },
            price: { price: 320, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/261819963",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/f20efcf2-b424-45f4-82bc-9b7ab181b75f/5fb4a74b-dce5-4751-b9e0-86012d321049.jpeg",
            classification: { is_bio: true },
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Lurpak Lighter Spreadable Butter Rapeseed Oil 400G",
            quantity: { grams: 400 },
            price: { price: 425, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/314427997",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/7c9c9ebb-9484-4aac-a9c7-7204d3281498/970f1ad4-f2bc-46e0-ac17-397c5592ec27_1277148902.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
      ],
    },
    {
      item_name: "Parmesan cheese",
      products: [
        {
          product: {
            product_name: "Creamfields Grana Padano Wedge 175G",
            quantity: { grams: 175 },
            price: { price: 249, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/304390832",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/efb80d0d-b5e2-47b2-8ba7-78dc4b4cba75/20e558f0-b6c8-4f5b-ae1f-0f8cde5a6e36_1738021218.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Parmigiano Reggiano 100G",
            quantity: { grams: 100 },
            price: { price: 280, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/276889389",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/c3566107-0b9f-441a-a18f-ea8c5829bdcb/7e96bdfb-a621-482c-95b4-20e9c706a5d6.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Finest Parmigiano Reggiano 170 G",
            quantity: { grams: 170 },
            price: { price: 385, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/276772509",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/35af8d09-e3cb-471e-94e2-1108aaaf4be5/bc48fe95-91e6-438c-b060-27c440e7db67.jpeg",
            classification: {},
          },
        },
      ],
    },
    {
      item_name: "Pasta",
      products: [
        {
          product: {
            product_name: "Hearty Food Co. Spaghetti Pasta 500g",
            quantity: { grams: 500 },
            price: { price: 28, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/297844134",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/23afec32-7192-4ff2-acfd-196f00b8a7d6/626aeae4-ef34-4904-9c7b-3bc5e88070c3_1755233342.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Free From Penne Pasta 500g",
            quantity: { grams: 500 },
            price: { price: 75, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/256876734",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/a8f16f82-a7b7-4a5f-a9b1-fd50bfcab158/96a1f0f9-fce0-4261-82fc-b1559ca81e65_2139140301.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Free From Spaghetti 500G",
            quantity: { grams: 500 },
            price: { price: 75, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/256876728",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/7b3ae3e7-472e-4a3c-992c-05a7f4ada694/a9f4c8f3-e4e9-4e14-bf72-3c9c35d568ee_1860527880.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Free From Macaroni",
            quantity: { grams: 500 },
            price: { price: 75, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/300916760",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/b4eb4984-ff0f-43a1-a865-28a549fa2185/37b0710e-1a4a-4737-ad53-3079f41f6b5c_192555780.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Short Spaghetti Pasta 500G",
            quantity: { grams: 500 },
            price: { price: 75, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/254878401",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/dd24290f-3a54-45e6-b88f-399ecc5cb9a5/3b6b6eec-ce96-4e0a-95c4-d3fc61694c88_1157947769.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Free From Lasagne Sheets 250g",
            quantity: { grams: 250 },
            price: { price: 75, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/264890284",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/22665a73-a806-4c70-9cb8-ba749d5a3064/9c293a23-cc0d-4616-8b1f-43c0ea9cbc95_1430927436.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Free From Tagliatelle 250G",
            quantity: { grams: 250 },
            price: { price: 75, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/282458361",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/b306f3c9-daf6-4250-bb37-6ce5f3b51bc5/6c5a7a29-c3f5-45e0-ab2d-3ed5924342da_1796963733.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Margheritine Soup Pasta 250G",
            quantity: { grams: 250 },
            price: { price: 90, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/277017009",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/3498534b-dd33-4ad5-80d8-1b1e588f7508/17aab74e-f850-4c7d-a58f-24cac7b1749c_263677215.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Finest Free From Linguine 400G",
            quantity: { grams: 400 },
            price: { price: 190, promotion: { promo: true } },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/317400140",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/a260233c-8699-4884-a659-c949cef9d68d/983ce052-a19d-497b-8f9c-0ecf27c899ce_1720428746.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Finest Free From Rigatoni 500G",
            quantity: { grams: 500 },
            price: { price: 190, promotion: { promo: true } },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/316941635",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/76779748-6e0f-4a80-afc3-437eee942282/8e32783f-de49-4afe-b928-4e78fc7a3811_1775319185.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Organic Spaghetti Pasta 500G",
            quantity: { grams: 500 },
            price: { price: 125, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/255874968",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/027b1166-85fd-48de-8380-ac7491c85675/ab10bb4d-725e-4743-8aa4-2e94bc239add_39338681.jpeg",
            classification: { is_bio: true },
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Organic Wholewheat Spaghetti 500g",
            quantity: { grams: 500 },
            price: { price: 125, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/262043041",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/bc2b59d0-c362-42f0-ac93-7e3f402464f0/1bc8fc5f-4264-4111-9183-6e05c7f0d56f_1428953917.jpeg",
            classification: { is_bio: true },
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Spaghetti Pasta 1Kg",
            quantity: { grams: 1000 },
            price: { price: 129, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/254878424",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/92368902-632b-458a-9e95-5771c68228c7/5ea5d542-4e7e-4974-ba33-856050b2a39b_1184442325.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Napolina Spaghetti Box 500G",
            quantity: { grams: 500 },
            price: { price: 150, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/308113228",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/a83f2c3d-0a46-46da-ac93-b3a6c4744809/75c52c1b-c829-45cd-a7a7-f88e8448ac12_1226130571.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Napolina Orzo Pasta 500g",
            quantity: { grams: 500 },
            price: { price: 150, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/317205550",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/c48d9f7c-eb1e-4836-a581-229e218ea71f/01d12040-1d9f-44e5-b87d-7565405bdaeb_1112540766.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Gluten Free Red Lentil Fusilli 250g",
            quantity: { grams: 250 },
            price: { price: 185, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/297484755",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/8e0e001e-609b-4c69-bea9-ba0f50a172dc/2398d0d2-6481-403a-9920-7b82dcd3dbc3_2112337025.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Tesco Finest Orzo Pasta 500G",
            quantity: { grams: 500 },
            price: { price: 215, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/268622118",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/d008c36d-08d4-45e7-a330-862b22b209b1/82cac8c2-622e-49c2-ac9c-62b50c78fe66_381063829.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Nissin Demae Ramen Noodles - Spicy 100g",
            quantity: { grams: 100 },
            price: { price: 75, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/276827043",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/f221dc9a-b545-4050-8550-924f651d8b55/0555e7b5-d9eb-4593-8a26-56d087659d78_1249392256.jpeg",
            classification: {},
          },
          num_units_to_buy: 3,
        },
        {
          product: {
            product_name: "Napolina Spaghetti Pasta 1Kg",
            quantity: { grams: 1000 },
            price: { price: 225, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/313368316",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/3c2c5c41-8780-44fb-bd3f-79b5588b0c9c/055886a6-f717-4ea5-9324-cd93bb87047d_1092351879.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
        {
          product: {
            product_name: "Rummo Gluten Free Spaghetti Pasta N0.3 400g",
            quantity: { grams: 400 },
            price: { price: 250, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/315465682",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/88d6ec72-8797-41e2-b58b-0d53e8dbb9b0/9e600372-94ad-4839-bf87-7f064489d283_1720350801.jpeg",
            classification: {},
          },
          num_units_to_buy: 1,
        },
      ],
    },
    {
      item_name: "Balsamic vinegar",
      products: [
        {
          product: {
            product_name: "Polli Pickled Red Onion in Balsamic Vinegar 190g",
            quantity: { grams: 190 },
            price: { price: 245, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/321764630",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/0054e396-c468-4135-a3c6-15af6a31e54f/7b54e0d4-8373-4b94-a993-a7b3c126e7f6_430177309.jpeg",
            classification: {},
          },
        },
      ],
    },
    {
      item_name: "Salt",
      products: [
        {
          product: {
            product_name: "Geo Organics Atlantic Sea Salt",
            quantity: { grams: 250 },
            price: { price: 135, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/253723108",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/861a8d6e-4480-4340-afc7-085e528d3faa/7f257c69-1b8e-4d00-bc80-4e90352c165a_1517586800.jpeg",
            classification: { is_bio: true },
          },
        },
        {
          product: {
            product_name: "Tesco 50% Less Sodium Salt 350G",
            quantity: { grams: 350 },
            price: { price: 140, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/260298744",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/008f3eea-ac4b-479f-bedf-a19391272087/9d28035c-174d-4c9d-b9d9-28138c13dc24_503105121.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Cornish Sea Salt Flakes 150g",
            quantity: { grams: 150 },
            price: { price: 150, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/302288208",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/85fa1e56-fa10-4bd1-9293-0cb765082bf0/c33b31e6-5e20-43e0-a338-03ea30f1a2e4_897629053.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Mediterranean Coarse Sea Salt 1kg",
            quantity: { grams: 1000 },
            price: { price: 180, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/326190347",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/marketplace/63934a35-df13-4acf-98ff-96efbd312605/139f41ab0afb414e91d6d697d0cd56d5_1219191144.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Saxa Salt 750G",
            quantity: { grams: 750 },
            price: { price: 190, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/251975227",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/106cd154-87c6-4df9-8f78-371a461fd99b/a68680ca-cc3b-4057-8012-918b76fd4593_631435706.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Saxa Coarse Sea Salt 350G",
            quantity: { grams: 350 },
            price: { price: 190, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/254193744",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/293f39ad-d57f-4460-8367-192e4a851ec0/f8350189-8a44-4ec3-b87d-78c7968fde3b_841200095.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Saxa Fine Sea Salt 350G",
            quantity: { grams: 350 },
            price: { price: 190, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/254065580",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/7e8ed1f3-8d7d-448e-a5ba-317bb87c27cf/3b3ca194-8776-40b3-98a8-e2098fdcb3c2_868836334.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tidmans Natural Rock Salt 500G",
            quantity: { grams: 500 },
            price: { price: 190, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/253729822",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/1fcacb66-29fb-4014-a849-9f0c9191d9ec/39ffca2d-73ca-4733-9e35-a00183940d7f_607038495.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Cooking Salt 1.5Kg",
            quantity: { grams: 1500 },
            price: { price: 195, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/258030678",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/a9917942-5aed-4e87-b170-b9e46496e3c6/fda753eb-96ef-4cfd-8a3e-2dedc89f8cd8_1615418742.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Cornish Sea Salt 225g",
            quantity: { grams: 225 },
            price: { price: 209, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/267680810",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/7804798d-2a81-459a-a532-5415b24fe359/0a9a3dc4-b7e2-4ada-b011-35c4eef83c84_1422253457.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Saxa So Low Reduced Sodium Salt 350G",
            quantity: { grams: 350 },
            price: { price: 215, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/253089478",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/24ac3e78-5b04-4656-b727-e3d30a3acd08/48429145-7eb9-4ef7-b37e-2220296ed515_1916272505.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Maldon Himalayan Pink Salt 250g",
            quantity: { grams: 250 },
            price: { price: 250, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/317056881",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/1c6969e5-ec75-4995-8e74-25e711b4256e/36508388-e0d0-41a1-ab93-7770f5d55ed3_978678636.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Rock Salt Grinder 100g",
            quantity: { grams: 100 },
            price: { price: 275, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/289130599",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/9b028eae-ffeb-440c-b34c-fc831d3fae61/04f966e7-a9c7-4351-8175-676edc34dde3_1218900700.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Maldon Sea Salt 250G",
            quantity: { grams: 250 },
            price: { price: 285, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/257410991",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/046ca3bc-b45c-42b1-9988-e12115f8280b/8a4f98a1-a3ba-4ef6-afc7-bf0732101c6f_841625329.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Maldon Sea Salt Flakes Grinder 55G",
            quantity: { grams: 55 },
            price: { price: 355, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/297021238",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/13c18b78-f88e-4737-871d-6f08113d85c2/2ff099ee-3cf7-47fe-bd4b-7ecb59bd5121_1867758569.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Traditional Unrefined Sea Salt 250g (Clearspring)",
            quantity: { grams: 250 },
            price: { price: 435, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/326197465",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/marketplace/9e34b379-515a-4739-a0b7-0450646ada56/fb52262f443c4d4f9d91241c269807dd_1004923171.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Minton & Donello Coarse Sea Salt No Additives",
            quantity: { grams: 3000 },
            price: {
              price: 1203,
              promotion: { promo: true, promo_percentage: 14 },
            },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/325795251",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/marketplace/4f654024-ea19-4579-96ca-61937cdd47f0/8bdbce2e122941a59afbe348059d388f_1523385613.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name:
              "Minton & Donello Fine Sea Salt No Additives 6 x 500g",
            quantity: { grams: 3000 },
            price: {
              price: 1232,
              promotion: { promo: true, promo_percentage: 14 },
            },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/330696072",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/marketplace/41e303a8-7b19-4434-863a-8e918f43919c/8bdbce2e122941a59afbe348059d388f_1522437981.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Minton & Donello Coarse Sea Salt",
            quantity: { grams: 4500 },
            price: {
              price: 1444,
              promotion: { promo: true, promo_percentage: 15 },
            },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/325795269",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/marketplace/9d3c8b95-bdc6-4ec0-92c3-3af0126a19f7/8bdbce2e122941a59afbe348059d388f_1523269493.jpeg",
            classification: {},
          },
        },
      ],
    },
    {
      item_name: "Black pepper",
      products: [
        {
          product: {
            product_name: "RAJAH GROUND BLACK PEPPER 100G",
            quantity: { grams: 100 },
            price: { price: 195, promotion: { promo: true } },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/321963089",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/09a80e28-83f3-4e87-aa6f-baefa71f632f/c650d209-a94d-4007-aa90-1f136fda524e_2058750908.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "RAJAH WHOLE BLACK PEPPER 100G",
            quantity: { grams: 100 },
            price: { price: 195, promotion: { promo: true } },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/322321807",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/ceeb30f4-65e7-4341-98a2-a74f1634ae0c/6fc0691c-f1e0-4d4a-ab89-c451944c1eb7_438182616.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Ground Black Pepper 25G",
            quantity: { grams: 25 },
            price: { price: 115, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/276545762",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/5a40708a-fb0d-475a-a0eb-8d3f3ef8c449/c3fbba08-33cc-4e1d-b394-5d4552de8ed2_1333118644.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name:
              "Schwartz Black Peppercorns Adjustable Medium grinder 35g",
            quantity: { grams: 35 },
            price: { price: 200, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/268589566",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/240e9706-2cf8-4adf-a162-9df1f28ed85d/f6107c08-04b3-4b8e-acdb-8a862a422c7d_248260389.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Whole Black Peppercorns 100G",
            quantity: { grams: 100 },
            price: { price: 285, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/256150815",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/d0d18d91-2666-4e31-9a75-a8e7b31aa156/ae8ab5eb-4ccf-4aaa-9a6f-fdc86b4023c7_732919147.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Black Peppercorn Grinder 50G",
            quantity: { grams: 50 },
            price: { price: 285, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/257724971",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/c1558ed0-2878-479f-a7d0-8ffebc2b0d6b/4430ee12-d8a7-4fc3-872a-e3dece1e915a_800212745.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Santa Maria Tellicherry Black Pepper Grinder 70G",
            quantity: { grams: 70 },
            price: { price: 290, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/279905188",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/2cedee85-7701-4975-9164-5f944c0e9f5b/e32a8158-45a2-468a-af29-21de4afcc05d_390671028.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Black Peppercorns 250G",
            quantity: { grams: 250 },
            price: { price: 440, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/301971870",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/d95fa377-2638-4d75-a778-100e9717bdea/df5638cf-4fda-4a66-bc6d-1ae84070d05d_2022594843.jpeg",
            classification: {},
          },
        },
        {
          product: {
            product_name: "Tesco Finest Tellicherry Pepper Corn Grinder 45G",
            quantity: { grams: 45 },
            price: { price: 490, promotion: {} },
            product_id:
              "https://www.tesco.com/groceries/en-GB/products/279683126",
            image_url:
              "https://digitalcontent.api.tesco.com/v2/media/ghs/c8a9792f-303e-4b03-9da0-050b44f93864/582e3e33-fa12-478b-a5be-1b0acd2d3341_1708729219.jpeg",
            classification: {},
          },
        },
      ],
    },
  ],
  currency: "GBP",
};

async function getData() {
  try {
    console.log("getting recipes!")
    const recipesResponse = await getRecipes();
    console.log("recipes got");
    console.log(recipesResponse);

    // get first recipe and its kg token
    const firstRecipe = recipesResponse.recipes[0];
    console.log({ firstRecipe });
    const kgToken = firstRecipe["kg_token"];
    console.log({ kgToken });

    // get products
    console.log("getting products");
    const products = await getProductsFromSupermarket(kgToken);
    console.log({ products });
    const cheapestProductList = getCheapestProductPerCategory(products);
    const cheapestProductIdQuantityPair =
      getProductIdPurchaseQuantityPair(cheapestProductList);

    console.log({ cheapestProductList });
    const sessionResponse = await getSession(cheapestProductIdQuantityPair);

    console.log("writing results");
    fs.writeFileSync("results/recipes.json", JSON.stringify(recipesResponse));
    fs.writeFileSync("results/products.json", JSON.stringify(products));
    fs.writeFileSync(
      "results/cheapestProducts.json",
      JSON.stringify(cheapestProductList)
    );
    fs.writeFileSync("results/session.json", JSON.stringify(sessionResponse));
    console.log("result written!");
  } catch (err) {
    console.error(err);
  } finally {
    const creditsRemaining = await getRemainingCredits();
    console.log({ creditsRemaining });
  }
}

const getRecipes = async () => {
  const dummyInput = [
    "Long-Life Milk",
    "Toiletries - Deodorant, Shampoo, Conditioner",
    "Tinned Vegetables - Carrots/Sweetcorn/Peas/Potatoes",
    "Tinned Fish",
    "Tinned Meat - Stew, Curry, Chilli, Chicken, Meatballs, Hotdogs",
    "Tinned Fruit",
    "Toilet Rolls",
    "Custard",
    "Cereals",
    "Pasta Sauce",
  ];
  const prompt = `This list comes from a food-bank and utilises pantry essentials. Please provide an accessible, simple, cheap and filling meals using the following ingredients only. ${dummyInput}. Do not use any fresh ingredients.`;

  const response = await fetch(`${ROOT_URL}/suggest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: BEARER,
    },
    body: JSON.stringify({ query: prompt }),
  });
  if (!response.ok) {
    throw new Error(`Response status: ${response.status}`);
  }

  const result = await response.json();
  return result;
};

const getProductsFromSupermarket = async (kgToken) => {
  const body = {
    recipe_kg_tokens: [kgToken],
    supermarket_domain: TARGET_SUPERMARKET_DOMAIN,
  };
  const response = await fetch(`${ROOT_URL}/products`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: BEARER,
    },
    body: JSON.stringify(body),
  });

  return response.json();
};

const getCheapestProductPerCategory = (products) => {
  return (products.items ?? [])
    .map((item) => {
      const cheapest = (item.products ?? []).reduce((best, current) => {
        const bestPrice =
          best?.product?.price?.price ?? Number.POSITIVE_INFINITY;
        const currPrice =
          current?.product?.price?.price ?? Number.POSITIVE_INFINITY;

        // If current is cheaper, replace best
        return currPrice < bestPrice ? current : best;
      }, null);

      return cheapest; // could be null if item.products empty
    })
    .map((product) => {
      console.log({ product });
      return { ...product, num_units_to_buy: product.num_units_to_buy ?? 1 };
    })
    .filter(Boolean); // remove nulls
};

const getProductIdPurchaseQuantityPair = (products) => {
  return products.map((product) => {
    console.log({ product });
    return {
      product: {
        product_id: product.product.product_id,
        num_units_to_buy: product.num_units_to_buy,
      },
    };
  });
};

const getSession = async (productQuantityPairs) => {
  const body = {
    items: productQuantityPairs,
    supermarket_domain: TARGET_SUPERMARKET_DOMAIN,
  };

  const response = await fetch(`${ROOT_URL}/session`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: BEARER,
    },
    body: JSON.stringify(body),
  });

  return await response.json();
};

const getRemainingCredits = async () => {
  const response = await fetch(`${ROOT_URL}/credits`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: BEARER,
    },
  });

  return await response.json();
};

getData();

Create Table user(
     id serial primary key,
     username TEXT NOT NULL unique,
);

Create table user_profile(
   user_id INTEGER PRIMARY KEY REFERENCES "user"(id) ON DELETE CASCADE,
   diet_type TEXT NOT NULL DEFAULT 'veg' CHECK (diet_type IN ('veg','egg','non_veg')),
   last_login_at TIMESTAMPTZ
);

Create table allergen(
   id serial primary key,
   allergen TEXT NOT NULL UNIQUE

);

Create table user_allergen(
   user_id INTEGET NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
   allergen_id INTEGER NOT NULL REFERENCES "allergen"(id) ON DELETE CASCADE,
   PRIMARY KEY (user_id, allergen_id)
);

Create table user cuisine preference(
  user_id NOT NULL REFERENCES "user"id ON DELETE CASCADE,
  cuisine TEXT NOT NULL,
  PRIMARY(user_id,cuisine)
);
Create table Ingredient(
 id SERIAL PRIMARY KEY,
 name TEXT NOT NULL UNIQUE,
 diet TEXT NOT NULL CHECK(diet in ( 'veg','egg','non_veg')),
 unit_kind TEXT NOT NULL CHECK(unit in ('count','weight','volume'))
);
Create TABLE Recipe(
  ID SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  cuisine TEXT NOT NULL UNIQUE,
  servinsg INTEGER NOT NULL (serving>0),
  prep_time INTEGER NOT NULL (prep_time>=0),
  cook_time INTEGER NOT NULL(cook_time>=0),
  total_time INTEGER NOT NULL(total_time>0),
  step_count INTEGER NOT NULL(step_count>0),
  diet_type NOT NULL CHECK(diet in ('veg','egg','non_veg')),
  complexity NOT NULL CHECK(complexity in('easy','medium','hard'))
);
CREATE TABLE recipe_ingredient (
    recipe_id INTEGER NOT NULL REFERENCES recipe(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredient(id) ON DELETE RESTRICT,
    quantity NUMERIC(10, 2) NOT NULL CHECK (quantity > 0),
    unit TEXT NOT NULL,
    PRIMARY KEY (recipe_id, ingredient_id)
);
CREATE TABLE recipe_steps (
    recipe_id INTEGER NOT NULL REFERENCES recipe(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL CHECK (step_number > 0),
    instruction TEXT NOT NULL,
    PRIMARY KEY (recipe_id, step_number)
);

CREATE TABLE pantry_item (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    ingredient_id INTEGER NOT NULL REFERENCES ingredient(id) ON DELETE RESTRICT,
    quantity NUMERIC(10, 2) NOT NULL CHECK (quantity >= 0),
    unit TEXT NOT NULL,
    expiry_date DATE,
    added_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE cook_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    recipe_id INTEGER NOT NULL REFERENCES recipe(id) ON DELETE RESTRICT,
    cooked_at TIMESTAMPTZ NOT NULL DEFAULT now()
);



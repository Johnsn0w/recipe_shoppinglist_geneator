from tkinter import *
from tkinter import ttk
from functools import partial
import pickle
import os.path


class Main_widget:
    """contains all elements"""

    def __init__(self, window):
        """init all the things"""
        self.frame_recipe_selection = ttk.LabelFrame(window, text="Select Recipe:")
        self.frame_recipe_selection.grid(column=0, row=0, sticky="n", padx=5, pady=5)
        self.frame_recipe_selection.config(relief=GROOVE)
        self.frame_recipe_selection.config(padding=(10, 10))

        self.frame_recipe_input = ttk.LabelFrame(window, text="Input New Recipe:")
        self.frame_recipe_input.grid(column=1, row=0, sticky="n", padx=5, pady=5)
        self.frame_recipe_input.config(relief=GROOVE)
        self.frame_recipe_input.config(padding=(10, 10))

        self.frame_recipe_input_col_0 = ttk.Frame(self.frame_recipe_input)
        self.frame_recipe_input_col_0.grid(column=1, row=1, sticky="n", padx=5, pady=5)
        self.frame_recipe_input_col_0.config(relief=GROOVE)
        self.frame_recipe_input_col_0.config(padding=(10, 10))

        self.frame_recipe_input_col_1 = ttk.Frame(self.frame_recipe_input)
        self.frame_recipe_input_col_1.grid(column=2, row=1, sticky="n", padx=5, pady=5)
        self.frame_recipe_input_col_1.config(relief=GROOVE)
        self.frame_recipe_input_col_1.config(padding=(10, 10))

        self.frame_recipe_input_col_2 = ttk.Frame(self.frame_recipe_input)
        self.frame_recipe_input_col_2.grid(column=3, row=1, sticky="n", padx=5, pady=5)
        self.frame_recipe_input_col_2.config(relief=GROOVE)
        self.frame_recipe_input_col_2.config(padding=(10, 10))

        self.frame_shopping_list = ttk.LabelFrame(window, text="Shopping List:")
        self.frame_shopping_list.grid(column=0, row=1, sticky="nw", padx=5, pady=5)
        self.frame_shopping_list.config(relief=GROOVE)
        self.frame_shopping_list.config(padding=(10, 10))

        self.entrybox_recipe = Entry(self.frame_recipe_input)  # entrybox_recipe variable
        self.entrybox_recipe.grid(column=1, row=0)

        self.entryboxes_ingredient = []  # entrybox_ingredient variable list
        self.entryboxes_quantity = []
        self.comboboxes_unit = []  # combobox_unit variable list
        self.new_ingredient_row()

        self.button_save_recipe = Button(self.frame_recipe_input, text="Save Recipe",
                                         command=self.save_new_recipe_to_db_file)
        self.button_save_recipe.grid(column=1, row=100)

        label_recipe_name = Label(self.frame_recipe_input, text="Recipe")  # label_recipe
        label_recipe_name.grid(column=0, row=0, sticky="n", pady=15)
        label_recipe_name = Label(self.frame_recipe_input, text="Ingredients")  # label_ingredients
        label_recipe_name.grid(column=0, row=1, sticky="n", pady=15)

        label_quantity = Label(self.frame_recipe_input, text="Quantity")  # label_quantity
        label_quantity.grid(column=2, row=0, pady=15)

        label_unit = Label(self.frame_recipe_input, text="Unit")  # label_unit
        label_unit.grid(column=3, row=0, pady=15)

        self.recipe_checkboxes = []
        self.load_db_into_checkboxs()

        self.error_message = StringVar()
        self.label_error = Label(self.frame_recipe_input, textvariable=self.error_message)

        # label_select_recipe
        # label_shopping_list

    class Recipe_checkbox:
        """Recipe Checkbox Object: all "recipies" are loaded into this class
        within we init a checkbox and the label objects. checkbox is displayed on init, ingredients are displayed on checkbox on/off
        """

        def __init__(self, recipe, frame_recipe_selection, frame_shopping_list):
            self.recipe_name = recipe[0]
            self.ingredients = recipe[1]
            self.frame_recipe_selection = frame_recipe_selection
            self.frame_shopping_list = frame_shopping_list
            self.displayed = False
            self.checkbox = Checkbutton(self.frame_recipe_selection, text=self.recipe_name,
                                        command=self.toggle_display_ingredients)
            self.checkbox.pack(anchor="w")

            self.ingredient_labels = []
            self.create_labels()

        def create_labels(self):
            """ingredient labels created, not displayed yet, current ingredients labels added to blank list"""
            for ingredient, values in self.ingredients.items():
                ingredient_label = Label(self.frame_shopping_list, text=ingredient)
                self.ingredient_labels.append(ingredient_label)

        def pack_or_unpack(self, option, label_toggle):
            if option == "pack":
                for ingredient in self.ingredient_labels:
                    # if label_toggle == ingred
                    pass

        def toggle_display_ingredients(self):
            """then loops through the list of labels, if checkbox is activated it displays them, if deactivated it undisplays them
            REFACTORED:
            """
            if self.displayed is False:
                for label in self.ingredient_labels:
                    label.pack()
                self.displayed = True
            else:
                for label in self.ingredient_labels:
                    label.pack_forget()
                self.displayed = False

    def new_ingredient_row(self, last_index=0, event=0):
        """create two entrybox widgets, and one combobox widget. Set focusing into the entrybox to call this function again, ignoring if not the last one created.
        append each new widget to respective list
        in other words, click the bottom entrybox and a fresh one below it is created
        """
        index = len(self.entryboxes_ingredient)
        last_index += 1
        if last_index >= index:
            new_ingredient = Entry(self.frame_recipe_input_col_0)
            new_ingredient.bind("<FocusIn>", partial(self.new_ingredient_row, index))
            new_ingredient.pack()
            self.entryboxes_ingredient.append([new_ingredient, index])

            new_quantity = Entry(self.frame_recipe_input_col_1)
            new_quantity.config(width=5)
            new_quantity.pack()
            self.entryboxes_quantity.append(new_quantity)

            new_unit = ttk.Combobox(self.frame_recipe_input_col_2)
            new_unit.config(width=10)
            new_unit.pack()
            self.comboboxes_unit.append(new_unit)

    def load_db_into_checkboxs(self):
        """loads recipes stored in storage.pkl file, puts each entry into a Recipe_checkbox class object, appends all created objects to the recipe_checkboxes list"""
        with open("storage.pkl", "rb") as storage_file:  # load storage.pkl into memory
            file_data = pickle.load(storage_file)
            for recipe in file_data:
                print(recipe)  # trace
                recipe_object = self.Recipe_checkbox(recipe, self.frame_recipe_selection, self.frame_shopping_list)
                self.recipe_checkboxes.append(recipe_object)

        # loop through each recipe object in memory:
        #   assign a varable of recipe_name = checkbox, checkbox event/?command= toggle_ingredients_display(self.recipe_name)
        #   append each new widget to recipe_labels
        #   <if my above event handling doesn't work then...> then set event to loop through recipe_label list VIA toggle_ingredients_display and if its varzable=1 then pack or pack_forget

    def save_new_recipe_to_db_file(self):
        """ saves new recipe to db and updates displayed checkboxs
        doesn't actually grab unit and quantity yet"""
        recipe_name = self.entrybox_recipe.get()
        recipe_dict = dict(self.entrybox_recipe.get())
        ingredients = []
        recipe = [recipe_name, recipe_dict]
        for ingredient in self.entryboxes_ingredient: # for loop through each box list + grab recipe_name
            ingredients.append(ingredient[0].get())
            recipe[1][ingredient[0].get()] = ["1", "gram"] # just temporary before I actually implement unit and quantity

        if ingredients == "" or recipe_name == "":
            self.display_error("Insufficient input, not saved")
        else:
            with open("storage.pkl", "rb") as storage_read: # with open storage.pkl as read, read contents to memory, append new recipe
                file_data = pickle.load(storage_read)
                file_data.append(recipe)

            with open("storage.pkl", "wb") as storage_write:# with open storage.pkl as write, write appended db list to pkl
                pickle.dump(file_data, storage_write)

            [checkbox.checkbox.pack_forget() for checkbox in self.recipe_checkboxes] # hacky, i refactor later
            self.load_db_into_checkboxs() # as above



    def display_error(self, error_text):
        self.error_message.set(error_text)
        self.label_error.grid(column=1, row=110)
        self.label_error.after(3000, lambda : self.label_error.grid_forget())
        # label_error_message.pack()
        # have any click event pack_forget() label_error_message
        pass


def main():
    window = Tk()
    Main_widget(window)
    window.mainloop()


main()

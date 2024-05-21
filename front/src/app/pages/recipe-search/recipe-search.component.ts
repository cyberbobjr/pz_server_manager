import {Component, OnInit} from '@angular/core';
import {CoreModule} from "@core/core.module";
import {FormsModule, ReactiveFormsModule, FormControl} from "@angular/forms";
import {CommonModule} from "@angular/common";
import {DisplaySourcePipe} from "./display-source.pipe";
import {MaterialModule} from "@app-material/material.module";
import recipesData from '../../../assets/all_recipes.json';
import {SourceDisplayComponent} from "./source-display/source-display.component";
import {debounceTime, Subject} from 'rxjs';
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";

interface Recipe {
  name?: string;
  sources: Source[];
  result: Result;
}

interface Source {
  items: Item[];
}

export interface Item {
  item: string;
  displayName: string;
  count: number;
  keep: boolean;
  destroy: boolean;
  use: number;
}

interface Result {
  item: string;
  displayName: string;
}

@Component({
  selector: 'app-recipe-search',
  standalone: true,
  imports: [
    CoreModule,
    FormsModule,
    ReactiveFormsModule,
    CommonModule,
    DisplaySourcePipe,
    MaterialModule,
    SourceDisplayComponent,
    MatProgressSpinnerModule
  ],
  templateUrl: './recipe-search.component.html',
  styleUrls: ['./recipe-search.component.scss']
})
export class RecipeSearchComponent implements OnInit {
  recipes: { [key: string]: Recipe } = recipesData;
  filteredRecipes: [string, Recipe][] = [];
  searchQuery = new FormControl('');
  private searchSubject: Subject<string> = new Subject<string>();
  isLoading: boolean = false;

  constructor() {
    this.searchSubject.pipe(debounceTime(2000)).subscribe(searchText => {
      this.filterRecipes(searchText);
      this.isLoading = false;
    });
  }

  ngOnInit(): void {
    this.searchQuery.valueChanges.subscribe(value => {
      this.isLoading = true;
      this.searchSubject.next(value!);
    });
    this.filterRecipes(this.searchQuery.value!);
  }

  filterRecipes(searchText: string): void {
    this.filteredRecipes = Object.entries(this.recipes).filter(([name, recipe]) => {
      const matchIngredient = recipe.sources.some(source =>
        source.items.some(ingredient => ingredient.displayName.toLowerCase().includes(searchText.toLowerCase()))
      );
      const matchResult = recipe.result.displayName.toLowerCase().includes(searchText.toLowerCase());
      return matchIngredient || matchResult;
    });
  }
}

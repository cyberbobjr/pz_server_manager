import {Component, OnInit} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";

@Component({
  selector: 'app-mods-index',
  templateUrl: './mods-index.component.html',
  styleUrl: './mods-index.component.scss'
})
export class ModsIndexComponent implements OnInit {

  constructor(private store: Store<{ pzStore: PzStore }>) {
  }

  ngOnInit(): void {
  }

}

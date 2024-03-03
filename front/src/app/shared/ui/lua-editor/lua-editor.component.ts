import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-lua-editor',
  templateUrl: './lua-editor.component.html',
  styleUrl: './lua-editor.component.scss'
})
export class LuaEditorComponent implements OnInit {
  editorOptions = {
    "autoIndent": true,
    "formatOnPaste": true,
    "formatOnType": true,
    theme: 'vs-dark',
    language: 'lua'
  };
  code: string = ``;

  constructor() {
  }

  ngOnInit(): void {

  }


}

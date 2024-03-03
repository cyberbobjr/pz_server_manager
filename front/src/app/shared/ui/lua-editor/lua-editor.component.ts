import {Component, forwardRef, Input} from '@angular/core';
import {ControlValueAccessor, NG_VALUE_ACCESSOR} from "@angular/forms";

@Component({
  selector: 'app-lua-editor',
  templateUrl: './lua-editor.component.html',
  styleUrl: './lua-editor.component.scss',
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => LuaEditorComponent),
      multi: true,
    },
  ],
})
export class LuaEditorComponent implements ControlValueAccessor {
  @Input() set language(language: string) {
    this.editorOptions.language = language;
  }

  onChange: (value: string) => void;
  onTouched: () => void;

  writeValue(value: string): void {
    this.code = value as string;
  }

  registerOnChange(fn: (value: string) => void): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  code: string | null = null;

  editorOptions = {
    "autoIndent": true,
    "formatOnPaste": true,
    "formatOnType": true,
    theme: 'vs-dark',
    language: 'lua'
  };
}

import {Pipe, PipeTransform} from '@angular/core';
import {Parser} from 'bulletin-board-code';

@Pipe({
  name: 'bbodeToHtml',
  standalone: true
})
export class BbodeToHtmlPipe implements PipeTransform {
  private parser: Parser;

  constructor() {
    this.parser = new Parser();
  }

  transform(value: string, ...args: unknown[]): unknown {
    return this.parser.toHTML(value);
  }

}

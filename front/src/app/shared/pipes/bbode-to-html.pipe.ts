import {Pipe, PipeTransform} from '@angular/core';
import {Parser} from 'bulletin-board-code';

@Pipe({
  name: 'bbcodeToHtml',
  standalone: true
})
export class BbcodeToHtmlPipe implements PipeTransform {
  private parser: Parser;

  constructor() {
    this.parser = new Parser();
  }

  transform(value: string, ...args: unknown[]): string {
    return value ? this.parser.toHTML(value) : '';
  }

}

import {Pipe, PipeTransform} from '@angular/core';
import {Item} from "./recipe-search.component";
import {DomSanitizer} from "@angular/platform-browser";

@Pipe({
  name: 'displaySource',
  standalone: true
})
export class DisplaySourcePipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) {
  }

  transform(value: { items: Item[] }, ...args: unknown[]): unknown {
    const html = value.items.map(item => {
      let classColor = item.keep ? 'keep' : 'destroy';
      return `<span class="${classColor}" matTooltip="${item.item}">${item.displayName} (${item.count})</span>`;
    }).join(', ');
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}

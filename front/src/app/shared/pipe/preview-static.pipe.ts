import {Pipe, PipeTransform} from '@angular/core';
import {environment} from '../../../environments/environment';

@Pipe({
  name: 'previewStatic'
})
export class PreviewStaticPipe implements PipeTransform {
  baseUrl = environment.baseUrl;

  transform(value: string, modpackname: string, modinfo: string): string {
    return `${this.baseUrl}/static/${modpackname}/${modinfo}/${value}`;
  }

}

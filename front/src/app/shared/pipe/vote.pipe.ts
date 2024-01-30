import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'vote'
})
export class VotePipe implements PipeTransform {

  transform(value: number, ...args: unknown[]): number {
    return Math.round((value * 10));
  }

}

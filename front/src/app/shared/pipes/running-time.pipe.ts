import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'runningTime',
  standalone: true
})
export class RunningTimePipe implements PipeTransform {

  transform(value: unknown, ...args: unknown[]): unknown {
    if (!value) {
      return null;
    }
    return (value as number) * 1000;
  }

}

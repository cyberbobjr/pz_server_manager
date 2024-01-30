import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-star-rating',
  templateUrl: './star-rating.component.html',
  styleUrls: ['./star-rating.component.scss']
})
export class StarRatingComponent {
  @Input() set rating(value: number) {
    this.stars = Array.from({length: 10}, (i, idx: number) => {
      return (idx < value) ? 'pi-star-fill' : 'pi-star';
    });
  }

  stars: string[] = [];
}

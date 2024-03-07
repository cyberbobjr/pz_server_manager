import {Component, Input} from '@angular/core';
import {Observable} from "rxjs";

@Component({
  selector: 'app-spinner',
  templateUrl: './spinner.component.html',
  styleUrl: './spinner.component.scss'
})
export class SpinnerComponent {
  @Input() isLoading: Observable<boolean>;
}

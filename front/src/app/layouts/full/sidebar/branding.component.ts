import {Component} from '@angular/core';

@Component({
  selector: 'app-branding',
  template: `
    <div class="branding">
      <a href="/">
        <img src="./assets/images/logos/logo.webp"
             style="width: 100%;max-width:150px"
             class="align-middle m-2"
             alt="logo"
        />
      </a>
    </div>
  `,
})
export class BrandingComponent {
  constructor() {
  }
}

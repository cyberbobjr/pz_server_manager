import {Component} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {PzAuthService} from "../../../core/services/pz-auth.service";
import {firstValueFrom} from "rxjs";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styles: [`
    :host ::ng-deep .pi-eye,
    :host ::ng-deep .pi-eye-slash {
      transform: scale(1.6);
      margin-right: 1rem;
      color: var(--primary-color) !important;
    }
  `]
})
export class LoginComponent {
  credentials: FormGroup = this.fb.group({
    username: [null, Validators.required],
    password: [null, Validators.required],
  })

  constructor(private fb: FormBuilder,
              private router: Router,
              private pzAuthService: PzAuthService) {
  }

  async login() {
    try {
      const response = await firstValueFrom(this.pzAuthService.login(this.credentials.value.username, this.credentials.value.password));
      this.pzAuthService.saveToken(response.token);
      await this.router.navigate(['/']);
    } catch (e) {

    }
  }
}

import { Component } from '@angular/core';
import { PzAuthService } from "@core/services/pz-auth.service";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { firstValueFrom } from "rxjs";
import { Router } from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
})
export class AppSideLoginComponent {
  loginForm: FormGroup = this.fb.group({
    username: [null, Validators.required],
    password: [null, Validators.required],
  })

  constructor(private pzAuthService: PzAuthService,
              private router: Router,
              private fb: FormBuilder) {
  }

  async login() {
    try {
      const result = await firstValueFrom(this.pzAuthService.login(this.loginForm.value.username, this.loginForm.value.password));
      this.pzAuthService.saveToken(result['token']);
      this.router.navigate(['/dashboard']);
    } catch (e) {

    }
  }
}

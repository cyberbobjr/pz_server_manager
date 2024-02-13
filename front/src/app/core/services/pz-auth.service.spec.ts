import { TestBed } from '@angular/core/testing';

import { PzAuthService } from './pz-auth.service';

describe('PzAuthService', () => {
  let service: PzAuthService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PzAuthService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

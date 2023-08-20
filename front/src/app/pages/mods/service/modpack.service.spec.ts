import { TestBed } from '@angular/core/testing';

import { ModpackService } from './modpack.service';

describe('ModpackService', () => {
  let service: ModpackService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ModpackService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

import {TestBed} from '@angular/core/testing';

import {PzServerService} from './pz-server.service';

describe('PzServerService', () => {
  let service: PzServerService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PzServerService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

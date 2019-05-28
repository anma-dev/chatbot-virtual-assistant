import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TryNowComponent } from './try-now.component';

describe('TryNowComponent', () => {
  let component: TryNowComponent;
  let fixture: ComponentFixture<TryNowComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TryNowComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TryNowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

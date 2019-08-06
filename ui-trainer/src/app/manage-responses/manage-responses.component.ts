import { Component, OnInit, Input, ViewChild, HostListener, OnDestroy } from '@angular/core';
import { WebSocketService } from '../common/services/web-socket.service';
import { EntitiesDataService } from '../common/services/entities-data.service';
import { SharedDataService } from '../common/services/shared-data.service';
import { NotificationsService } from '../common/services/notifications.service';
import { constant } from '../../environments/constants';
import { MatInput } from '@angular/material/input';
import { Subscription } from 'rxjs';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-manage-responses',
  templateUrl: './manage-responses.component.html',
  styleUrls: ['./manage-responses.component.scss']
})
export class ManageResponsesComponent implements OnInit, OnDestroy {

  text_entities: Array<string>;
  text_entities_backup: any;
  entities: any;
  entities_backup: any;
  new_response_text: string;
  showEntityDropdown = false;
  show_empty_entity_error = false;
  readonly = false;
  currentResponse: any;
  appSource: string;

  private subscription: Subscription = new Subscription();

  @Input() responseObjectId: string;
  @Input() projectObjectId: string;

  @ViewChild('responseText') responseTextInput: MatInput;

  constructor(private entities_service: EntitiesDataService,
              private webSocketService: WebSocketService,
              public sharedDataService: SharedDataService,
              public notificationsService: NotificationsService) { }

  ngOnInit() {
    this.appSource = environment.app_source;
    this.text_entities = new Array<string>();
    this.getEntities();
    this.getResponseDetails();
    this.sharedDataService.setSharedData('activeTabIndex', '1', constant.MODULE_COMMON);
  }

  getEntities() {
    this.entities_service.createEntitiesRoom();
    this.entities_service.getEntities({project_id: this.projectObjectId}).subscribe(entities => {
      this.entities = this.entities_backup = entities;
    },
    err => console.error('Observer got an error: ' + err),
    () => console.log('Observer got a complete notification'));
  }

  getResponseDetails() {
    this.webSocketService.createResponseRoom('response_' + this.responseObjectId);
    // tslint:disable-next-line: max-line-length
    this.webSocketService.getResponseDetails({object_id: this.responseObjectId}, 'response_' + this.responseObjectId).subscribe(response_details => {
      this.currentResponse = response_details;
      this.text_entities = this.text_entities_backup = this.currentResponse.text_entities;
    },
    err => console.error('Observer got an error: ' + err),
    () => console.log('Observer got a complete notification'));

    this.subscription.add(this.webSocketService.getResponseDetailsAlerts().subscribe(intent_details => {
      this.notificationsService.showToast(intent_details);
    },
    err => console.error('Observer got an error: ' + err),
    () => console.log('Observer got a complete notification')));
  }

  addResponseTextElement(event: any) {
    if (this.new_response_text.trim() !== '') {
      const new_response_text_arr = this.new_response_text.split(' ');
      for (let i = 0; i < new_response_text_arr.length; i++) {
        if (new_response_text_arr[i].includes('@')) {
          new_response_text_arr[i] = new_response_text_arr[i].replace('@', '{');
          new_response_text_arr[i] += '}';
        }
      }
      this.new_response_text = new_response_text_arr.join(' ');
      // tslint:disable-next-line: max-line-length
      this.webSocketService.createResponseText({object_id: this.responseObjectId, text_entities: this.new_response_text}, 'response_' + this.responseObjectId);
      this.new_response_text = '';
      if (event.which === 13) {
        event.preventDefault();
      }
    }
  }

  removeResponseTextElement(index: number, text_entity: string) {
    // tslint:disable-next-line: max-line-length
    this.webSocketService.deleteResponseText({object_id: this.responseObjectId, text_entities: text_entity}, 'response_' + this.responseObjectId);
  }

  applyMapFilter(filterValue: string) {
    this.text_entities = this.text_entities_backup;
    this.text_entities = this.text_entities.filter((value) => {
      if (value.includes(filterValue.trim())) {
        return value;
      }
    });
  }

  applyEntityFilter(filterValue: string) {
    this.entities = this.entities_backup;
    this.entities = this.entities.filter((value) => {
      if (value.entity_name.includes(filterValue.trim())) {
        return value;
      }
    });
  }

  populateEntities(event: any) {
    if (event.which === 50 && event.key === '@') {
      if (this.entities.length > 0) {
        this.showEntityDropdown = true;
      } else {
        this.show_empty_entity_error = true;
      }
      this.readonly = true;
    } else if (event.which === 222) {
      this.new_response_text = this.new_response_text.slice(0, -1);
    }
  }

  selectEntity(entity: string) {
    this.new_response_text = this.new_response_text + entity + ' ';
    this.showEntityDropdown = false;
    this.readonly = false;
    this.responseTextInput.focus();
  }

  @HostListener('document:keyup', ['$event'])
  handleDeleteKeyboardEvent(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      this.new_response_text = this.new_response_text.slice(0, -1);
      this.showEntityDropdown = false;
      this.readonly = false;
      this.show_empty_entity_error = false;
    }
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }

}

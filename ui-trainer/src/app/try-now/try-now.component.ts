import { Component, OnInit, OnDestroy } from '@angular/core';
import { WebSocketService } from '../common/services/web-socket.service';
import { SharedDataService } from '../common/services/shared-data.service';
import { constant } from '../../environments/constants';

declare var adjustTryNowScroll: Function;
declare var changeRowBackgroundColor: Function;

@Component({
  selector: 'app-try-now',
  templateUrl: './try-now.component.html',
  styleUrls: ['./try-now.component.scss']
})
export class TryNowComponent implements OnInit, OnDestroy {

  projectObjectId: string;
  showSpinner: boolean;
  chats: Array<object>;
  chats_backup: Array<object>;
  userChatMessage: string;
  trackerStore: any;

  showUserBotCardDetails: boolean;
  userBotCardType: string;
  userBotCardText: string;
  private userBotCardTime;
  userBotCardIntent: string;
  userBotCardConfidence: string;

  storyCode: any;
  predictions: any;
  showUserPredictionsDetails: boolean;
  slots: any;

  constructor(public webSocketService: WebSocketService,
              public sharedDataService: SharedDataService) { }

  ngOnInit() {
    this.projectObjectId = this.sharedDataService.getSharedData('projectObjectId', constant.MODULE_COMMON);
    this.showSpinner = true;
    this.showUserBotCardDetails = false;
    this.showUserPredictionsDetails = true;
    this.tryNowProject();
  }

  tryNowProject() {
    this.webSocketService.createTryNowRoom('try_now');
    this.webSocketService.tryNowProject(this.projectObjectId).subscribe(response => {
      if (response.status === 'Success') {
        this.showSpinner = false;
        this.chats = new Array<object>();
        this.chats_backup = new Array<object>();
        this.chats.push({event: 'action', name: 'action_listen'});
      }
    },
    err => console.error('Observer got an error: ' + err),
    () => console.log('Observer got a complete notification'));
  }

  sendChat(send_message?: string) {
    if (send_message !== undefined) {
      this.userChatMessage = send_message;
    }
    if (this.userChatMessage.trim() !== '') {
      this.webSocketService.chatNowProject(this.userChatMessage).subscribe(response => {
        if (response) {
          this.chats = this.chats_backup = this.storyCode = response['tracker-store']['events'];
          // tslint:disable-next-line: max-line-length
          this.predictions = {text: response['tracker-store']['latest_message']['text'], intent_ranking: response['tracker-store']['latest_message']['intent_ranking']};
          this.slots = response['tracker-store']['slots'];
          adjustTryNowScroll();
        }
      },
      err => console.error('Observer got an error: ' + err),
      () => console.log('Observer got a complete notification'));
      this.userChatMessage = '';
    }
  }

  selectRowIndex(chat_row_index: number) {
    changeRowBackgroundColor(chat_row_index);
    if (this.chats[chat_row_index]['event'] === 'user') {
      this.userBotCardType = 'M';
      this.userBotCardText = this.chats[chat_row_index]['text'];
      this.userBotCardTime = new Date(Math.floor(this.chats[chat_row_index]['timestamp'])  * 1000);
      this.userBotCardIntent = this.chats[chat_row_index]['parse_data']['intent']['name'];
      this.userBotCardConfidence = this.chats[chat_row_index]['parse_data']['intent']['confidence'];
      // tslint:disable-next-line: max-line-length
      this.predictions = {text: this.chats[chat_row_index]['parse_data']['text'], intent_ranking: this.chats[chat_row_index]['parse_data']['intent_ranking']};
      this.showUserBotCardDetails = true;
      this.showUserPredictionsDetails = true;
    } else if (this.chats[chat_row_index]['event'] === 'bot') {
      this.userBotCardType = 'B';
      this.userBotCardText = this.chats[chat_row_index]['text'];
      this.userBotCardTime = new Date(Math.floor(this.chats[chat_row_index]['timestamp'])  * 1000);
      this.userBotCardIntent = '';
      this.userBotCardConfidence = '';
      this.predictions = {text: '', intent_ranking: ''};
      this.showUserBotCardDetails = true;
      this.showUserPredictionsDetails = false;
    } else if (this.chats[chat_row_index]['event'] === 'action') {
      this.predictions = {text: '', intent_ranking: ''};
      this.showUserBotCardDetails = false;
      this.showUserPredictionsDetails = false;
    }
    this.storyCode = this.chats_backup.slice(0, chat_row_index + 1);
  }

  ngOnDestroy(): void {
    window.location.reload();
  }

}

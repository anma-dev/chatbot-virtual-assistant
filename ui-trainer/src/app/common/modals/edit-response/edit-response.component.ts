import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { FormControl, Validators, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-edit-response',
  templateUrl: './edit-response.component.html',
  styleUrls: ['./edit-response.component.scss']
})
export class EditResponseComponent implements OnInit {

  editResponseForm: FormGroup;

  constructor(public dialogRef: MatDialogRef<EditResponseComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any) { }

  ngOnInit() {
    this.editResponseForm = new FormGroup({
      responseName: new FormControl({value: this.data.responseName, disabled: true}, Validators.required),
      responseDescription: new FormControl(this.data.responseDescription, Validators.required)
    });
  }

  closeDialog() {
    if (this.editResponseForm.valid) {
      this.dialogRef.close({
        project_id: this.data.projectObjectId,
        domain_id: this.data.domainObjectId,
        object_id: this.data.responseObjectId,
        response_name: this.editResponseForm.value.responseName,
        response_description: this.editResponseForm.value.responseDescription
      });
    }
  }
}

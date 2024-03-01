import {Component} from '@angular/core';
import {Store} from "@ngrx/store";
import {PzStore} from "@pzstore/reducers/server.reducer";
import {PzStatus} from "../../../core/interfaces/PzStatus";
import {Observable} from "rxjs";
import {CommonModule} from "@angular/common";
import {RunningTimePipe} from "../../pipes/running-time.pipe";

@Component({
    selector: 'app-server-status',
    standalone: true,
    imports: [
        CommonModule,
        RunningTimePipe
    ],
    templateUrl: './server-status.component.html',
    styleUrl: './server-status.component.scss'
})
export class ServerStatusComponent {
    status$: Observable<PzStatus | null>;

    constructor(private store: Store<{ pzStore: PzStore }>) {
        this.status$ = this.store.select(store => store.pzStore.status);
    }
}

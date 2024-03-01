import {Component, OnInit} from '@angular/core';
import {navItems} from './sidebar-data';

@Component({
    selector: 'app-sidebar',
    templateUrl: './sidebar.component.html',
})
export class SidebarComponent implements OnInit {
    navItems = navItems;

    constructor() {
    }

    ngOnInit(): void {
    }
}

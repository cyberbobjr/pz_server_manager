import {Pipe, PipeTransform} from '@angular/core';

@Pipe({
  name: 'extractModInfos',
  standalone: true
})
export class ExtractModInfosPipe implements PipeTransform {

  transform(value: string, ...args: unknown[]): { modIds: string[], mapFolders: string[] } {
    return this.extractValues(value);
  }

  private extractValues(inputText: string): { modIds: string[], mapFolders: string[] } {
    const modIdRegex = /Mod ID: (.+)/g;
    const mapFolderRegex = /Map Folder: (.+)/g;

    let match;
    const modIds: string[] = [];
    const mapFolders: string[] = [];

    // Extract all Mod IDs
    while ((match = modIdRegex.exec(inputText)) !== null) {
      modIds.push(match[1]);
    }

    // Extract all Map Folders
    while ((match = mapFolderRegex.exec(inputText)) !== null) {
      mapFolders.push(match[1]);
    }

    return {modIds, mapFolders};
  };
}

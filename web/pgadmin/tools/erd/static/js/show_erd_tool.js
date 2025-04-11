/////////////////////////////////////////////////////////////
//
// pgAdmin 4 - PostgreSQL Tools
//
// Copyright (C) 2013 - 2025, The pgAdmin Development Team
// This software is released under the PostgreSQL Licence
//
//////////////////////////////////////////////////////////////
import pgWindow from 'sources/window';
import {getPanelTitle} from 'tools/sqleditor/static/js/sqleditor_title';
import {getRandomInt} from 'sources/utils';
import url_for from 'sources/url_for';
import gettext from 'sources/gettext';
import React from 'react';
import ReactDOM from 'react-dom/client';
import ERDTool from './erd_tool/components/ERDTool';
import ModalProvider from '../../../../static/js/helpers/ModalProvider';
import Theme from '../../../../static/js/Theme';
import { BROWSER_PANELS } from '../../../../browser/static/js/constants';
import { NotifierProvider } from '../../../../static/js/helpers/Notifier';
import usePreferences, { listenPreferenceBroadcast } from '../../../../preferences/static/js/store';
import pgAdmin from 'sources/pgadmin';
import { PgAdminProvider } from '../../../../static/js/PgAdminProvider';
import { getPanelUrl } from './ERDModule';
import pgBrowser from 'pgadmin.browser';


  // Callback to draw ERD Tool for objects
  export function relaunchErdTool(state_info) {
    let connection_info = state_info.connection_info,
    tool_data = state_info.tool_data;
    let parentData = {
        server_group: {
          _id: connection_info.sgid || 0,
          server_type: connection_info.server_type
        },
        server: {
          _id: connection_info.sid,
        },
        database: {
          _id: connection_info.did,
        },
        schema: {
          _id: connection_info.scid || null,

        },
        table: {
            _id: connection_info.tid || null,
        }
      };
  
    
    const transId = getRandomInt(1, 9999999);
    const panelTitle = '';
    //const panelUrl = getPanelUrl(transId, parentData, connection_info.gen);

    let openUrl = url_for('erd.panel', {
          trans_id: transId,
        });
    
        openUrl += `?sgid=${parentData.server_group._id}`
          +`&sid=${parentData.server._id}`
          +`&server_type=${parentData.server.server_type}`
          +`&did=${parentData.database._id}`
          +`&gen=${connection_info.gen}`;
    
        if(parentData.schema) {
          openUrl += `&scid=${parentData.schema._id}`;
        }
        if(parentData.table) {
          openUrl += `&tid=${parentData.table._id}`;
        }
        const panelUrl = openUrl;

    const open_new_tab = usePreferences.getState().getPreferencesForModule('browser').new_browser_tab_open;
    let sqlId = `old_qt_data${state_info.id}`;
    let params = {sql_id: sqlId}
    
    pgAdmin.Browser.Events.trigger(
      'pgadmin:tool:show',
      `${BROWSER_PANELS.ERD_TOOL}_${transId}`,
      panelUrl,
      {...params, title: _.escape(panelTitle)},
      {title: 'Untitled', icon: 'fa fa-sitemap'},
      Boolean(open_new_tab?.includes('erd_tool'))
    );
    localStorage.setItem(sqlId, tool_data);
    return true;
  }
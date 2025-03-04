from pgadmin.utils.ajax import make_json_response
from pgadmin.model import db, QueryToolDataModel
from config import MAX_QUERY_HIST_STORED
import json


class SaveQueryToolData:
    @staticmethod
    def get_saved_query_tool_data(uid):
        res = []
        result = (db.session \
            .query(QueryToolDataModel.uid,
                   QueryToolDataModel.trans_id,
                   QueryToolDataModel.connection_info,
                  QueryToolDataModel.query_data)
            .filter(QueryToolDataModel.uid == uid))
        for rec in list(result):
                res.append({
                    'old_trans_id': rec.trans_id,
                    'connection_info': rec.connection_info,
                    'query_data': rec.query_data
                })
        return make_json_response(success=1,  errormsg='', data=res)

    # @staticmethod
    # def update_query_tool_data(uid, sid, dbname, trans_id, request):
    #     #SaveQueryToolData.get(uid, sid, dbname, trans_id)


    @staticmethod
    def save(uid, trans_id, connection_info, query_data ):
        try:
            data_entry = QueryToolDataModel(trans_id=trans_id, uid=uid,
                connection_info=connection_info, query_data=query_data)

            db.session.merge(data_entry)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            # do not affect query execution if history saving fails

        return make_json_response(
            data={
                'status': True,
                'msg': 'Success',
            }
        )

    @staticmethod
    def clear_query_tool_data(uid, trans_id):
        try:
            filters = [
                QueryToolDataModel.uid == uid,
                QueryToolDataModel.trans_id == trans_id
            ]

            history = db.session.query(QueryToolDataModel) \
                .filter(*filters)
            # for row in history:
            #     query_info = json.loads(row.query_data.decode())
            #     print(query_info)
            history.delete()
            # for row in history:
            #     query_info = json.loads(row.query_data.decode())
            #     print(query_info)
            #     if query_info['query'] == filter['query'] and \
            #         query_info['start_time'] == filter['start_time']:
            #         db.session.delete(row)
            # if filter is not None:
            #     for row in history:
            #         query_info = json.loads(row.query_info.decode())
            #         print(query_info)
            #         if query_info['query'] == filter['query'] and \
            #                 query_info['start_time'] == filter['start_time']:
            #             db.session.delete(row)
            # else:
            #     history.delete()

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            # do not affect query execution if history clear fails

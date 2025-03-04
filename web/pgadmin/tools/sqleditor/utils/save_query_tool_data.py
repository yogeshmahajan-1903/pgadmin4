from pgadmin.utils.ajax import make_json_response
from pgadmin.model import db, QueryToolDataModel
from config import MAX_QUERY_HIST_STORED
import json


class SaveQueryToolData:
    @staticmethod
    def get(uid):
        res = []
        result = (db.session \
            .query(QueryToolDataModel.uid,
                   QueryToolDataModel.connection_info,
                  QueryToolDataModel.query_data)
            .filter(QueryToolDataModel.uid == uid))
        for rec in list(result):
                res.append({
                    'uid': rec.connection_info,
                    'query_data': rec.query_data
                })

        print(res)
        return make_json_response(
            data={
                'status': True,
                'msg': '',
                'result': res
            }
        )

    # @staticmethod
    # def update_query_tool_data(uid, sid, dbname, trans_id, request):
    #     #SaveQueryToolData.get(uid, sid, dbname, trans_id)


    @staticmethod
    def save(uid, sid, dbname, trans_id, request):
        SaveQueryToolData.get(uid)
        try:
            # max_srno = db.session \
            #     .query(db.func.max(QueryToolDataModel.srno)) \
            #     .filter(QueryToolDataModel.uid == uid,
            #             QueryToolDataModel.sid == sid,
            #             QueryToolDataModel.dbname == dbname,
            #             QueryToolDataModel.trans_id == trans_id) \
            #     .scalar()
            #
            # # if no records present
            # if max_srno is None:
            #     new_srno = 1
            # else:
            #     new_srno = max_srno + 1
            #
            #     # last updated flag is used to recognise the last
            #     # inserted/updated record.
            #     # It is helpful to cycle the records
            #     last_updated_rec = db.session.query(QueryToolDataModel) \
            #         .filter(QueryToolDataModel.uid == uid,
            #                 QueryToolDataModel.sid == sid,
            #                 QueryToolDataModel.dbname == dbname,
            #                 QueryToolDataModel.trans_id == trans_id,
            #                 QueryToolDataModel.last_updated_flag == 'Y') \
            #         .first()
            #
            #     # there should be a last updated record
            #     # if not present start from sr no 1
            #     if last_updated_rec is not None:
            #         last_updated_rec.last_updated_flag = 'N'
            #
            #         # # if max limit reached then recycle
            #         # if new_srno > MAX_QUERY_HIST_STORED:
            #         #     new_srno = (last_updated_rec.srno % MAX_QUERY_HIST_STORED) + 1
            #     else:
            #         new_srno = 1
            #
            #     # if the limit is lowered and number of records present is
            #     # more, then cleanup
            #     if max_srno > MAX_QUERY_HIST_STORED:
            #         db.session.query(QueryToolDataModel) \
            #             .filter(QueryToolDataModel.uid == uid,
            #                     QueryToolDataModel.sid == sid,
            #                     QueryToolDataModel.dbname == dbname,
            #                     QueryToolDataModel.srno >
            #                     MAX_QUERY_HIST_STORED) \
            #             .delete()

            data_entry = QueryToolDataModel(trans_id=trans_id, uid=uid,
                query_data=request.data.query_data, connection_info=request.data.query_data.connections_list)

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
    def clear_query_tool_data(uid, trans_id, sid=None, dbname=None, filter=None):
        try:
            filters = [
                QueryToolDataModel.uid == uid,
                QueryToolDataModel.trans_id == trans_id
            ]

            history = db.session.query(QueryToolDataModel) \
                .filter(*filters)
            for row in history:
                query_info = json.loads(row.query_data.decode())
                print(query_info)
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

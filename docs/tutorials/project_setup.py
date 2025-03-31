import mlrun
import os
from mlrun.datastore.datastore_profile import DatastoreProfileV3io, DatastoreProfileKafkaSource, TDEngineDatastoreProfile


def setup(
        project: mlrun.projects.MlrunProject,
) -> mlrun.projects.MlrunProject:
    
    # Setting model monitoring creds
    
    tsdb_profile = DatastoreProfileV3io(name="v3io-tsdb-profile") 
    stream_profile = DatastoreProfileV3io(name="v3io-stream-profile",
                                        v3io_access_key=mlrun.mlconf.get_v3io_access_key())

    if mlrun.mlconf.is_ce_mode():
        mlrun_namespace = os.environ.get('MLRUN_NAMESPACE', 'mlrun')
        tsdb_profile = TDEngineDatastoreProfile(name="tdengine-tsdb-profile",
                                                user='root',
                                                password='taosdata',
                                                host=f'tdengine.{mlrun_namespace}.svc.cluster.local',
                                                port='6041')
    
        stream_profile = DatastoreProfileKafkaSource(
            name="kafka-stream-profile",
            brokers=f'my-kafka.{mlrun_namespace}.svc.cluster.local:9092',topics=[]
        )

    project.register_datastore_profile(stream_profile)
    project.register_datastore_profile(tsdb_profile)


    project.set_model_monitoring_credentials(
    tsdb_profile_name=tsdb_profile.name,
    stream_profile_name=stream_profile.name,
    )

    return project


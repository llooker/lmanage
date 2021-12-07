import logging
import coloredlogs
import looker_sdk
from create_folder_permissions import create_folder_permissions as cfp
from create_user_permissions import user_permission as up
from utils import group_config as gc
from utils import folder_config as fc
from utils import parse_yaml as py

logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO')


def main(**kwargs):
    div = '--------------------------------------'

    ini_file = kwargs.get("ini_file")
    yaml_path = kwargs.get("yaml_config_path")
    logger.info(div)
    logger.info('parsing yaml file')
    yaml = py.Yaml(yaml_path=yaml_path)
    instance_config = yaml.read_provision_yaml()
    sdk = looker_sdk.init31(config_file=ini_file)

###############################################################
# Group Config ################################################
###############################################################
    # # FIND UNIQUE GROUPS FROM YAML FILE
    unique_group_names = gc.get_unique_groups(parsed_yaml=instance_config)
    logger.info(div)

    # # CREATE NEW GROUPS
    group_metadata = gc.get_group_metadata(
        sdk=sdk, unique_group_list=unique_group_names)
    logger.info(div)

    # # DELETE ALL GROUPS THAT DO NOT MATCH WITH YAML
    gc.sync_groups(group_name_list=unique_group_names,
                   group_metadata_list=group_metadata, sdk=sdk)
    logger.info(div)

###############################################################
# Role Config ################################################
###############################################################
    # # FIND UNIQUE ROLES
    # # CREATE NEW ROLES
    # # ATTACH ROLES TO TEAM GROUPS
    # # DELETE ALL ROLES THAT DON'T MATCH WITH YAML

###############################################################
# Folder Config ################################################
###############################################################
    # # FIND UNIQUE FOLDERS
    unique_folder_names = fc.get_unique_folders(
        sdk=sdk, parsed_yaml=instance_config)
    logger.info(div)

   # # CREATE NEW FOLDERS
    folder_metadata = fc.get_folder_metadata(
        sdk=sdk, unique_folder_list=unique_folder_names)
    logger.info(div)

    # # CONFIGURE FOLDERS WITH EDIT AND VIEW ACCESS
    # folder_permission_metadata = cfp.folder_output(
    #     sdk=sdk,
    #     group_metadata=group_metadata,
    #     group_config=group_config)

    # # DELETE ALL FOLDERS THAT DON'T MATCH WITH YAML
    fc.sync_folders(sdk=sdk, folder_metadata_list=folder_metadata,
                    folder_name_list=unique_folder_names)
    logger.info(div)


    # # update content access
    # logger.info(div)
    # logger.info('Adding content access...')
    # cfp.provision_folders_with_group_access(
    #     sdk,
    #     folder_permission_metadata=folder_permission_metadata)
    # # create roles
    # logger.info(div)
    # logging.info('Creating Roles')
    # role_metadata = up.create_role_mapping(group_config=group_config)
    # role_create = up.create_roles(sdk=sdk, role_mapping=role_metadata)
    # up.attach_role_to_group(sdk=sdk, role_metadata=role_create,
    #                         group_config=group_config)
    # # removing all user group from folders
    # logger.info(div)
    # logger.info('Removing all user group from folders')
    # up.remove_all_user_group(
    #     sdk=sdk, folder_permission_metadata=folder_permission_metadata)
if __name__ == "__main__":
    YP = ('/usr/local/google/home/hugoselbie/code_sample/py/'
          'lmanage/tests/example_yamls/fullinstance.yaml')
    IP = ('/usr/local/google/home/hugoselbie/code_sample/py/ini/k8.ini')

    main(
        ini_file=IP,
        yaml_config_path=YP)
    logger.info('I have finished')
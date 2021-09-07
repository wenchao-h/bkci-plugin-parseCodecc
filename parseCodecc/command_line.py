# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import python_atom_sdk as sdk
from .error_code import ErrorCode

import os, glob, shutil
import json

err_code = ErrorCode()


def exit_with_error(error_type=None, error_code=None, error_msg="failed"):
    """
    @summary: exit with error
    """
    if not error_type:
        error_type = sdk.OutputErrorType.PLUGIN
    if not error_code:
        error_code = err_code.PLUGIN_ERROR
    sdk.log.error("error_type: {}, error_code: {}, error_msg: {}".format(error_type, error_code, error_msg))

    output_data = {
        "status":    sdk.status.FAILURE,
        "errorType": error_type,
        "errorCode": error_code,
        "message":   error_msg,
        "type":      sdk.output_template_type.DEFAULT
    }
    sdk.set_output(output_data)

    exit(error_code)


def exit_with_succ(data=None, quality_data=None, msg="run succ"):
    """
    @summary: exit with succ
    """
    if not data:
        data = {}

    output_template = sdk.output_template_type.DEFAULT
    if quality_data:
        output_template = sdk.output_template_type.QUALITY

    output_data = {
        "status":  sdk.status.SUCCESS,
        "message": msg,
        "type":    output_template,
        "data":    data
    }

    if quality_data:
        output_data["qualityData"] = quality_data

    sdk.set_output(output_data)

    sdk.log.info("finish")
    exit(err_code.OK)


def main():
    """
    @summary: main
    """
    # 输入
    input_params = sdk.get_input()

    local_path = input_params.get("local_path", None)
    if not local_path:
        exit_with_error(error_type=sdk.output_error_type.USER,
                        error_code=err_code.USER_CONFIG_ERROR,
                        error_msg="local_path is None")
    sdk.log.info("local path is {}".format(local_path))

    # 自定义codecc文件名通配，兼容codecc后续版本的改动
    codecc_glob = sdk.get_sensitive_conf("codecc_glob")
    if codecc_glob is None:
        codecc_glob = "codecc_*.json"

    # 插件逻辑
    os.chdir(sdk.get_workspace())
    if not os.path.exists(local_path):
        exit_with_error(error_type=sdk.output_error_type.USER,
                        error_code=err_code.USER_CONFIG_ERROR,
                        error_msg="local_path does not exists")

    json_list = glob.glob(os.path.join(local_path, codecc_glob))
    if len(json_list) != 1:
        exit_with_error(error_type=sdk.output_error_type.USER,
                        error_code=err_code.USER_CONFIG_ERROR,
                        error_msg="number of codecc json file must be 1")
    
    json_file = json_list[0]
    sdk.log.info("json file is {}".format(json_file))

    total_serious = 0
    total_normal = 0
    total_prompt = 0

    with open(json_file, "r") as f:
        json_body = json.load(f)
        build_id = json_body["bs_build_id"]
        real_build_id = sdk.get_pipeline_build_id()
        if build_id != real_build_id:
            error_msg = "build_id is {build_id}, real_build_id is {real_build_id}, they are not the same".format(build_id=build_id, real_build_id=real_build_id)
            exit_with_error(error_type=sdk.output_error_type.USER,
                            error_code=err_code.USER_CONFIG_ERROR,
                            error_msg=error_msg)
        
        for tool in json_body["tool_snapshot_list"]:
            if "total_serious" in tool:
                total_serious += tool["total_serious"]
            if "total_normal" in tool:
                total_normal += tool["total_normal"]
            if "total_prompt" in tool:
                total_prompt += tool["total_prompt"]
    sdk.log.info("total_serious is {total_serious}, total_normal is {total_normal}, total_prompt is {total_prompt}".format(total_serious=total_serious, total_normal=total_normal, total_prompt=total_prompt))
    try:
        shutil.rmtree(local_path)
    except OSError as e:
        sdk.log.error(str(e))

    # 插件执行结果、输出数据
    data = {
        "total_serious": {
            "type": sdk.output_field_type.STRING,
            "value": str(total_serious)
        },
        "total_normal": {
            "type": sdk.output_field_type.STRING,
            "value": str(total_normal)
        },
        "total_prompt": {
            "type": sdk.output_field_type.STRING,
            "value": str(total_prompt)
        }
    }
    exit_with_succ(data=data)

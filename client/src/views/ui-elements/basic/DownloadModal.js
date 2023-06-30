import axios from "axios";
import fileDownload from "js-file-download";
import React from 'react';
import Popup from 'reactjs-popup';
import "./DownloadModal.css"

export const DownloadModal = ((data) => {
    const outputFileList = data?.outputFileList

    const downloadList = outputFileList ? outputFileList.map((file, idx) => {
        let content = file['content']
        let resultImage = null
        if (file['content_type'] === 'image/png') {
            content = Uint8Array.from(atob(file['content']), c => c.charCodeAt(0));
            resultImage = <img width="200px" src={'data:image/png;base64,' + file['content']}/>
        }

        const blob = new Blob([content], {type: file['content_type']});
        const fileUrl = URL.createObjectURL(blob);
        const filename = file['filename']

        const handleDownload = (url, filename) => {
            axios.get(url, {
                responseType: 'blob',
            })
                .then((res) => {
                    fileDownload(res.data, filename)
                })
        }

        return (<div className="pl-2">
            <button className="text-xs text-blueGray-500 py-1 " onClick={() => {
                handleDownload(fileUrl, filename)
            }}> {filename}</button>
            {resultImage ? <p className="text-xs text-blueGray-300">[Preview]</p> : null}
            {resultImage}
        </div>)

    }) : null

    return (
        <div>
            <Popup
                trigger={<button className="hover:text-blueGray-700 pr-1 pt-1 text-sm text-blueGray-400"> Click here to download the results </button>}
                modal
                className="my-popup"
            >
                {close => (
                        <div className="popup_modal">
                            <button className="close text-blueGray-500" onClick={close}>
                                &times;
                            </button>
                            <div className="header text-blueGray-500">
                                Step-by-Step Results
                                <div className="text-xs text-blueGray-400"> Click the individual file to download.
                                </div>
                                <div className="text-xs text-blueGray-400 pb-2"> * Please ensure that you download all
                                    the
                                    files prior to making any adjustments to the pipeline.
                                </div>
                            </div>
                            <div className="content">
                                {downloadList}
                            </div>
                        </div>
                )}
            </Popup>
        </div>)
});
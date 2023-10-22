"use client"
import React from 'react'


type RenderedComponentType = {
    code: string
    component: any
    prompt: string
}


const DisplayComponent = ({
    code,
    component,
    prompt
}: RenderedComponentType) => {
    return (
        <div>
            <h1>{prompt}</h1>
            {component}
        </div>
    )
}

export default DisplayComponent
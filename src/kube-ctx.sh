#!/usr/bin/env bash
header='{"items": ['
footer=']}'
current_context=$(sh -c "cat $kube_config_path | yq '.current-context'")
contexts=$(cat << EOB
	{
		"title": "$current_context",
		"subtitle": "current context",
		"arg": "$current_context"
	},
EOB
)

for context in $(sh -c "cat $kube_config_path | yq '.contexts[] .name'");
do
contexts=$contexts$(cat << EOB
	{
		"title": "$context",
		"arg": "$context"
	},
EOB
);
done

echo $header$contexts$footer

#!/bin/bash
watch -d -n .5 'tail -n 50 logs/control.out.log | tac | awk "/^======/{p=1;next} /Display/{exit} p" | tac | column -t -s ":" | sed s/\*//'
